<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="keywords" content="">
  <meta name="description" content="">
  <meta name="robots" content="noindex">
  <link rel="icon" href="{{ relative_path(absolute='/static/img/favicon.ico', cwd=str_Cwd) }}" >
  <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha256-MBffSnbbXwHCuZtgPYiwMQbfE7z+GOZ7fBPCNB06Z98=" crossorigin="anonymous"> -->
  <link href="{{ relative_path(absolute='/static/css/bootstrap_custom.css', cwd=str_Cwd) }}" rel="stylesheet">
  <link href="{{ relative_path(absolute='/static/css/bootstrap-icons.min.css', cwd=str_Cwd) }}" rel="stylesheet">
  <link href="{{ relative_path(absolute='/static/css/transition.css', cwd=str_Cwd) }}" rel="stylesheet">
  <title>{% block title %}{% endblock %}</title>
</head>
<body>
  <header class="sticky-top">
    <nav class="navbar navbar-expand-md navbar-dark bg-secondary">
      <div class="container-fluid">
        <a class="navbar-brand" href="{{ relative_path(absolute='/', cwd=str_Cwd) }}">
          <img src="{{ relative_path(absolute='/static/img/logo.svg', cwd=str_Cwd) }}" width="200" alt="週7日本語 ロゴ">
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav pt-2">
            {% for dct_Day in lst_Days %}
            {% set int_DayId = loop.index0 %}
            {# 注 特殊な変数loopに対してレシーバindex0を呼び出すことで0始まりの現在の繰り返し回数を取得できる #}
            {#    参考 https://www.gesource.jp/weblog/?p=3527 #}
            {% set str_BunchAbsPath = '/bunch/' ~ dct_Day['symbol'] %} {# 引数absoluteに渡す変数BunchAbsPathを設定 #}
            {# 注 `~`で文字列や数値を結合できる  #}
            <li class="nav-item light" style="font-weight: 700;">
              <a class="nav-link fs-4 py-1 text-center {% if int_TargetDayId is defined and int_TargetDayId == int_DayId %}active{% endif %}" href="{{ relative_path(absolute=str_BunchAbsPath, cwd=str_Cwd) }}">{{ dct_Day['name_ja'] }}</a>
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main class="bg-success text-white">
    <div class="d-grid col-sm-9 col-md-8 col-lg-7 col-xxl-6 mx-auto px-3 py-4 px-md-0">
      {% block content %}{% endblock %}
    </div>
  </main>

  <footer class="bg-secondary text-center text-white py-3 px-5 mt-0">
    <div class="container">
      <div class="row py-2">
        <div class="py-1 col-lg-6">
          <a class="link-light" href="/">ホームへ</a>
        </div>
        <div class="py-1 col-lg-6">
          <a class="link-light" href="#">このページの先頭へ</a>
        </div>
      </div>
    </div>
    <div class="py-1">
      &copy; 2024 ky5bass
    </div>
  </footer>
  
  <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha256-gvZPYrsDwbwYJLD5yeBfcNujPhRoGOY831wwbIzz3t0=" crossorigin="anonymous"></script> -->
  <script src="{{ relative_path(absolute='/static/js/bootstrap.bundle.min.js', cwd=str_Cwd) }}"></script>
</body>
</html>