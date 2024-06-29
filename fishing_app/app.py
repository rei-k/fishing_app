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

@app.route('/select-season', methods=['GET', 'POST'])
def select_season():
    if request.method == 'POST':
        selected_season = request.form.get('season')
        if selected_season:
            selection['season'] = selected_season
            # 季節に基づいて正しいエンドポイント名を生成
            endpoint = f'select_fish_{selected_season.lower()}'
            return redirect(url_for(endpoint))
    seasons = Season.query.all()
    return render_template('select_season.html', seasons=seasons)

def select_fish_by_season(season_name):
    if request.method == 'POST':
        selected_fish = request.form.get('fish')
        if selected_fish:
            selection['fish'] = selected_fish
            return redirect(url_for('select_rod'))
    season = Season.query.filter_by(name=season_name.capitalize()).first()
    if season:
        season_fish = SeasonFish.query.filter_by(season_id=season.id).all()
        fish_ids = [sf.fish_id for sf in season_fish]
        available_fish = Fish.query.filter(Fish.id.in_(fish_ids)).all()
        return render_template(f'select_fish_{season_name}.html', fish=available_fish)
    return redirect(url_for('select_season'))

@app.route('/select-fish-spring', methods=['GET', 'POST'])
def select_fish_spring():
    return select_fish_by_season("spring")

@app.route('/select-fish-summer', methods=['GET', 'POST'])
def select_fish_summer():
    return select_fish_by_season("summer")

@app.route('/select-fish-autumn', methods=['GET', 'POST'])
def select_fish_autumn():
    return select_fish_by_season("autumn")

@app.route('/select-fish-winter', methods=['GET', 'POST'])
def select_fish_winter():
    return select_fish_by_season("winter")

@app.route('/select-rod', methods=['GET', 'POST'])
def select_rod():
    if request.method == 'POST':
        selected_rod = request.form.get('rod')
        if selected_rod:
            selection['rod'] = selected_rod
            return redirect(url_for('select_bait'))
    fish = Fish.query.filter_by(name=selection['fish']).first()
    if fish:
        fish_rod = FishRod.query.filter_by(fish_id=fish.id).all()
        rod_ids = [fr.rod_id for fr in fish_rod]
        available_rods = Rod.query.filter(Rod.id.in_(rod_ids)).all()
        return render_template('select_rod.html', rods=available_rods)
    return redirect(url_for('select_fish_spring'))  # デフォルトで春の魚選択ページにリダイレクト

@app.route('/select-bait', methods=['GET', 'POST'])
def select_bait():
    if request.method == 'POST':
        selected_bait = request.form.get('bait')
        if selected_bait:
            selection['bait'] = selected_bait
            return redirect(url_for('result'))
    rod = Rod.query.filter_by(name=selection['rod']).first()
    if rod:
        fish_bait = FishBait.query.filter_by(fish_id=selection['fish']).all()
        bait_ids = [fb.bait_id for fb in fish_bait]
        available_baits = Bait.query.filter(Bait.id.in_(bait_ids)).all()
        return render_template('select_bait.html', baits=available_baits)
    return redirect(url_for('select_rod'))

@app.route('/result')
def result():
    return render_template('result.html', selection=selection)

if __name__ == '__main__':
    app.run(debug=True)
