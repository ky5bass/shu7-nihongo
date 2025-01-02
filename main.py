from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from supabase import create_client
import shutil
from os.path import relpath
from os import environ
from datetime import timedelta
from datetime import datetime as _datetime

obj_distDirPath = Path(__file__).parent / 'public'  # 注 このディレクトリの中身は空であるものとして以下進める
obj_srcDirPath  = Path(__file__).parent / 'static'
obj_tplDirPath  = Path(__file__).parent / 'templates'

str_supabaseUrl = environ['SUPABASE_URL']
str_supabaseKey = environ['SUPABASE_KEY']

def relative_path(
    absolute: str,
    cwd: str,
) -> str:
    """cwdに対するabsoluteの相対パスを取得"""

    # 引数のバリデーションチェック
    if '/' != absolute[0]: raise ValueError(f"argument 'absolute' must start with '/': {absolute}")
    if '/' != cwd[0]:      raise ValueError(f"argument 'cwd' must start with '/': {cwd}")
    
    # 相対パスを取得
    str_retPath = relpath(absolute, cwd)

    return str_retPath

def main():
    # ソースディレクトリを丸ごとコピー
    shutil.copytree(obj_srcDirPath, obj_distDirPath / obj_srcDirPath.name)

    # 出力先ディレクトリ内にbunchディレクトリを作成
    obj_distBunchDirPath = obj_distDirPath / 'bunch'
    obj_distBunchDirPath.mkdir()

    # supabaseクライアントを用意
    obj_supabaseClient = create_client(str_supabaseUrl, str_supabaseKey)

    # 曜日ディクショナリを取得
    dct_days = dict()
    obj_db_res_0 = (
        obj_supabaseClient.table('days')
        .select('*')
        .order('id')
        .execute()
    )   # 参考 https://supabase.com/docs/reference/python/select
    for obj_entry in obj_db_res_0.data:
        str_day_symbol = obj_entry['name'][:3].lower()  # 例) sun
        dct_days[str_day_symbol] = obj_entry

    # レンダリングの準備
    obj_env = Environment(loader=FileSystemLoader(obj_tplDirPath), trim_blocks=False)
    obj_env.globals['relative_path'] = relative_path    # テンプレにrelative_path関数を埋め込み
    # 参考 関数埋め込みの方法→ https://gist.github.com/snaka/2575718

    # 本日のdaySymbolを取得
    obj_now = _datetime.now() + timedelta(hours=+9)
    # 注 9時間後にすることで日本時間に変換
    int_todayNo = obj_now.weekday()     # 月曜=>0, ..., 日曜=>6
    lst_daySymbols = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    str_todaySymbol = lst_daySymbols[int_todayNo]

    # トップページをレンダリング
    obj_template = obj_env.get_template('index.tpl')
    str_output = obj_template.render(
        days=dct_days,
        today_symbol=str_todaySymbol,
        cwd='/',)
    obj_outputPath = obj_distDirPath / 'index.html'
    with obj_outputPath.open('wt') as f:
        f.write(str_output)
    # 参考 extendsの方法→ https://www.python.ambitious-engineer.com/archives/809

    for str_daySymbol in dct_days:
        # dayIdを取得
        int_dayId: int = dct_days[str_daySymbol]['id']

        # カードを取得
        obj_db_res_1 = (
            obj_supabaseClient.rpc('bunch', params={'_day_id': int_dayId})
            .order('number')
            .execute()
        )   # 参考 https://supabase.com/docs/reference/python/rpc
        lst_cards: list = obj_db_res_1.data

        # 更新日付を取得
        str_dateRaw = dct_days[str_daySymbol]['cards_updated_at']
        obj_tmpDtm = _datetime.strptime(str_dateRaw, r'%Y-%m-%d')
        str_date = obj_tmpDtm.strftime(r'%Y年%-m月%-d日')
        # 注 %-m %-d で月日を1桁で表現できる。ただしUnix環境に依存しており、Windowsなら %#m %#d らしい。
        #    参考 https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0#answer-2073189

        # bunchページをレンダリング
        obj_template = obj_env.get_template('bunch.tpl')
        str_output = obj_template.render(
            days=dct_days,
            cards=lst_cards,
            created_date=str_date,
            this_day_symbol=str_daySymbol,
            cwd='/bunch',)
        obj_outputPath = obj_distDirPath / f'bunch/{str_daySymbol}.html'
        with obj_outputPath.open('wt') as f:
            f.write(str_output)

if __name__ == '__main__':
    main()