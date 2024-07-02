from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fishing_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデルの定義
class Season(db.Model):
    season_id = db.Column(db.Integer, primary_key=True)
    season_name = db.Column(db.String(50), nullable=False)

class Fish(db.Model):
    fish_id = db.Column(db.Integer, primary_key=True)
    fish_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(50))
    habitat = db.Column(db.String(200))
    bait = db.Column(db.String(200))
    gear = db.Column(db.String(200))
    rod_image = db.Column(db.String(50))
    bait_image = db.Column(db.String(50))
    season = db.Column(db.String(50))

# 初期データの挿入
def insert_initial_data():
    db.create_all()
    if Fish.query.count() == 0:
        fish_data = [
            {"fish_name": "アマゴ", "image": "amago.jpg", "habitat": "冷たい山間部の清流", "bait": "イクラ, ミミズ, 虫（クロカワムシ、カワゲラ）", "gear": "初心者: 短めの渓流竿（3.6m）、小型スピニングリール、4lbライン", "rod_image": "beginner_rod.jpg", "bait_image": "ikura.jpg", "season": "春"},
            {"fish_name": "ニジマス", "image": "nijimasu.jpg", "habitat": "清流や渓流", "bait": "ペレット, ミミズ, 虫（カワゲラ）", "gear": "初心者: 3.6mの渓流竿、4lbライン、小型スピニングリール", "rod_image": "beginner_rod.jpg", "bait_image": "mimizu.jpg", "season": "春"},
            {"fish_name": "ウグイ", "image": "ugui.jpg", "habitat": "清流や中流域", "bait": "ミミズ, イクラ, 練り餌", "gear": "初心者: 2.7mの小型の竿、ナイロンライン、ウキ釣りセット", "rod_image": "beginner_rod.jpg", "bait_image": "ikura.jpg", "season": "春"},
            {"fish_name": "ハヤ", "image": "haya.jpg", "habitat": "清流や中流域", "bait": "ミミズ, パン, 練り餌", "gear": "初心者: 2.7mの小型の竿、ナイロンライン、ウキ釣りセット", "rod_image": "beginner_rod.jpg", "bait_image": "pan.jpg", "season": "春"},
            {"fish_name": "アユ", "image": "ayu.jpg", "habitat": "大きな川の中流域", "bait": "友釣り用の生きたアユ, イクラ", "gear": "初心者: 友釣り用の9mのアユ竿、ナイロンライン、ウキ仕掛け", "rod_image": "ayu_rod.jpg", "bait_image": "ikura.jpg", "season": "夏"},
            {"fish_name": "テナガエビ", "image": "tenagaebi.jpg", "habitat": "河口付近の汽水域", "bait": "ミミズ, 小さなエビ, 練り餌", "gear": "初心者: 1.8mのエビ用竿、細いナイロンライン、小型ウキ", "rod_image": "ebi_rod.jpg", "bait_image": "ebi.jpg", "season": "夏"},
            {"fish_name": "オイカワ", "image": "oikawa.jpg", "habitat": "清流や中流域", "bait": "ミミズ, 練り餌, 虫（アカムシ）", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "mushi.jpg", "season": "夏"},
            {"fish_name": "ナマズ", "image": "namazu.jpg", "habitat": "中流から下流域、湖沼", "bait": "ミミズ, 小魚, エビ", "gear": "初心者: 3mの強めの竿、ナイロンライン、ウキ仕掛け", "rod_image": "strong_rod.jpg", "bait_image": "ebi.jpg", "season": "夏"},
            {"fish_name": "イワナ", "image": "iwana.jpg", "habitat": "冷たい山間部の渓流", "bait": "ミミズ, イクラ, 虫（カゲロウの幼虫）", "gear": "初心者: 3.6mの渓流竿、小型スピニングリール、4lbライン", "rod_image": "beginner_rod.jpg", "bait_image": "mimizu.jpg", "season": "秋"},
            {"fish_name": "カワムツ", "image": "kawamutsu.jpg", "habitat": "中流から下流域", "bait": "ミミズ, 練り餌, パン", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "pan.jpg", "season": "秋"},
            {"fish_name": "ブラックバス", "image": "blackbass.jpg", "habitat": "湖沼や緩やかな流れのある川", "bait": "ワーム, 小魚, 虫（カゲロウの幼虫）", "gear": "初心者: 2.7mのベイトロッド、ナイロンライン、スピナーベイト", "rod_image": "bait_rod.jpg", "bait_image": "worm.jpg", "season": "秋"},
            {"fish_name": "ニゴイ", "image": "nigoi.jpg", "habitat": "中流から下流域", "bait": "ミミズ, 練り餌, イクラ", "gear": "初心者: 3mの竿、ナイロンライン、ウキ仕掛け", "rod_image": "strong_rod.jpg", "bait_image": "mimizu.jpg", "season": "冬"},
            {"fish_name": "コイ", "image": "koi.jpg", "habitat": "河口付近や大きな川の中流域", "bait": "ミミズ, 練り餌, パン", "gear": "初心者: 3.6mの強めの竿、ナイロンライン、ウキ仕掛け", "rod_image": "strong_rod.jpg", "bait_image": "pan.jpg", "season": "冬"},
            {"fish_name": "フナ", "image": "funa.jpg", "habitat": "池や湖、緩やかな流れのある川", "bait": "練り餌, ミミズ, パン", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "pan.jpg", "season": "冬"},
            {"fish_name": "ヤツメウナギ", "image": "yatsumeunagi.jpg", "habitat": "冷たい清流や渓流", "bait": "ミミズ, 小魚, 練り餌", "gear": "初心者: 2.7mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "mimizu.jpg", "season": "冬"},
        ]
        for fish in fish_data:
            new_fish = Fish(**fish)
            db.session.add(new_fish)
        db.session.commit()

# 初期データの挿入
with app.app_context():
    insert_initial_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fish/<season>')
def fish(season):
    season_map = {
        'all': '全ての季節',
        'spring': '春',
        'summer': '夏',
        'autumn': '秋',
        'winter': '冬'
    }
    season_name = season_map.get(season, '全ての季節')
    if season == 'all':
        fish_list = Fish.query.all()
    else:
        fish_list = Fish.query.filter_by(season=season_name).all()
    return render_template('fish.html', fish_list=fish_list, season_name=season_name)

if __name__ == '__main__':
    app.run(debug=True)
