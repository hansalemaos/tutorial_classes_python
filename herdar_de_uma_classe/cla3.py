import urllib
from time import sleep
from textwrapre import wrapre
from a_selenium2df import get_df
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def split_text(text):
    return wrapre(
        " ".join(text.splitlines()),
        blocksize=4000,
        regexsep=r"\.",
        raisewhenlonger=False,
        removenewlines_from_result=True,
    )

def translate(text, langsrc, langdst):
    splitted = split_text(text)
    driver = uc.Chrome(headless=True)
    results = []
    for s in splitted:
        yandexlink = f'''https://translate.yandex.com/?source_lang={langsrc}&target_lang={langdst}&text={urllib.parse.quote(s)}'''
        driver.get(yandexlink)
        sleep(1)
        checkval = 0
        while checkval < 0.5:
            try:
                while len(driver.find_elements(By.TAG_NAME, "pre")) < 1:
                    sleep(1)
                df=get_df(
                    driver,
                    By,
                    WebDriverWait,
                    expected_conditions,
                    queryselector="span",
                    with_methods=True,
                )
                df2 = df.loc[df.aa_outerHTML.str.contains('fullTextTranslation', na=False)]
                translatedtext = df2.aa_innerText.iloc[0]
                lentranslated = len(translatedtext)
                checkval = lentranslated / len(s) > .5
                results.append(translatedtext)
            except Exception:
                sleep(1)
                continue
    driver.close()
    driver.quit()
    return results


text_de = """The New York Times (NYT) ist eine einflussreiche überregionale US-amerikanische Tageszeitung, die in New York City im Verlag der New York Times Company erscheint."""
result=translate(text_de, langsrc='de', langdst='pt')
print(result)
