#chromeとchromedriverはともにversion103を使用しています。
#ブラウザのバージョンが更新されたらドライバーを上書きして、定数CHROMEDRIVERの値を変更してください
#各所で入るsleepは表示の待ち時間です。PCのスペックや通信環境によっては調整する必要があります。
from argparse import Action
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# id、名前、参照パス
WORKSPASE = "ワークスペース名"
MAIL = "xxxxx"
PASSWORD = "xxxx"
TEAMS_URL = 'チャネルへのURL'
SLACK_URL = 'チャネルへのURL'
CHROMEDRIVER = "ドライバーへのパス"

#ブラウザ通知をオフ、マイクとカメラの使用も許可する
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--use-fake-ui-for-media-stream")

 
# ブラウザを開く
teams_browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=CHROMEDRIVER)
 
# teamsのチャネルにアクセス
teams_browser.get(TEAMS_URL)
sleep(3)

# emailボックス入力
elem = teams_browser.find_element(By.NAME, 'loginfmt')
elem.send_keys(MAIL + Keys.RETURN)
sleep(3)
#password入力
elem = teams_browser.find_element(By.NAME, 'passwd')
elem.send_keys(PASSWORD + Keys.RETURN)
sleep(3)

#いいえをクリック
teams_browser.find_element(By.ID, 'idBtn_Back').click()
sleep(8)

# 会議ボタンを押下
# クラス名で取得しているが、将来的にはxpassの方が汎用性が高いかもしれない。
teams_browser.find_element(By.CLASS_NAME, 'app-title-bar-button').click()
sleep(3)

# マイクミュート
teams_browser.find_element(By.ID, 'preJoinAudioButton').click()
sleep(3)

# 今すぐ参加を押下
teams_browser.find_element(By.CLASS_NAME, 'join-btn').click()
sleep(10)

# リンクをコピーして　
teams_browser.find_element(By.ID, 'meeting_share_panel_copy_meeting_link').click()
sleep(3)

# slack用で別途ブラウザを開き、ログイン画面を開く
slack_browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=CHROMEDRIVER)
slack_browser.get(SLACK_URL)
sleep(5)

# ワークスペース入力
elem = slack_browser.find_element(By.ID, 'domain')
elem.send_keys(WORKSPASE + Keys.RETURN)
sleep(5)

# emailbox入力
elem = slack_browser.find_element(By.ID, 'email')
elem.send_keys(MAIL)
sleep(3)

# password入力
elem = slack_browser.find_element(By.ID, 'password')
elem.send_keys(PASSWORD + Keys.RETURN)
sleep(6)

# 検索ボックスを特定し、リンクとメッセージを入力
elem = slack_browser.find_element(By.CLASS_NAME, 'ql-editor')
elem.send_keys('会議室へのURLです' + Keys.RETURN + Keys.CONTROL, 'v')
slack_browser.find_element(By.CLASS_NAME, 'c-wysiwyg_container__button--send').click()
sleep(3)


# 9時間経過後にブラウザを閉じる、あとはタスクスケジューラーで自動スリープさせる
sleep(60*60*9)
teams_browser.quit()
slack_browser.quit()