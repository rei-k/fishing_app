# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fishing_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデルの定義
class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

class Rod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

class Bait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

class SeasonFish(db.Model):
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), primary_key=True)
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'), primary_key=True)

class FishRod(db.Model):
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'), primary_key=True)
    rod_id = db.Column(db.Integer, db.ForeignKey('rod.id'), primary_key=True)

class FishBait(db.Model):
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'), primary_key=True)
    bait_id = db.Column(db.Integer, db.ForeignKey('bait.id'), primary_key=True)

# テーブルの作成
with app.app_context():
    db.create_all()

# 選択された情報を保持する辞書
selection = {
    "season": None,
    "fish": None,
    "rod": None,
    "bait": None
}

@app.route('/select_season', methods=['GET', 'POST'])
def select_season():
    seasons = Season.query.all()  # 全ての季節を取得
    if request.method == 'POST':
        selected_season = request.form.get('season')
        if selected_season:
            # 季節に基づいて正しいエンドポイント名を生成
            endpoint = f'select_fish_{selected_season.lower()}'
            # リダイレクト先のエンドポイント名が正しいものか確認
            if endpoint in ['select_fish_spring', 'select_fish_summer', 'select_fish_autumn', 'select_fish_winter']:
                return redirect(url_for(endpoint))
    return render_template('select_season.html', seasons=seasons)

def select_fish_by_season(season_name):
    season = Season.query.filter_by(name=season_name.capitalize()).first()
    if season:
        season_fish = SeasonFish.query.filter_by(season_id=season.id).all()
        fish_ids = [sf.fish_id for sf in season_fish]
        available_fish = Fish.query.filter(Fish.id.in_(fish_ids)).all()
        return render_template(f'select_fish_{season_name.lower()}.html', fish=available_fish)
    return redirect(url_for('select_season'))

@app.route('/select_fish_spring', methods=['GET', 'POST'])
def select_fish_spring():
    return select_fish_by_season("spring")

@app.route('/select_fish_summer', methods=['GET', 'POST'])
def select_fish_summer():
    return select_fish_by_season("summer")

@app.route('/select_fish_autumn', methods=['GET', 'POST'])
def select_fish_autumn():
    return select_fish_by_season("autumn")

@app.route('/select_fish_winter', methods=['GET', 'POST'])
def select_fish_winter():
    return select_fish_by_season("winter")

if __name__ == '__main__':
    app.run(debug=True)
