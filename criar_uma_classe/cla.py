# pip install a-selenium2df textwrapre undetected-chromedriver

import urllib
from time import sleep
from textwrapre import wrapre
from a_selenium2df import get_df
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
def translate(text, langsrc, langdst):
    splitted = wrapre(
        " ".join(text.splitlines()),
        blocksize=4000,
        regexsep=r"\.",
        raisewhenlonger=True,
        removenewlines_from_result=True,
    )
    driver = uc.Chrome(headless=True)
    results = []
    for s in splitted:
        googlelink = f"https://translate.google.com/?sl={langsrc}&tl={langdst}&text={urllib.parse.quote(s)}&op=translate"
        driver.get(googlelink)
        sleep(1)
        checkval = 0
        while checkval < 0.5:
            try:
                while len(driver.find_elements(By.TAG_NAME, "textarea")) < 2:
                    sleep(1)
                    continue
                df = get_df(
                    driver,
                    By,
                    WebDriverWait,
                    expected_conditions,
                    queryselector="textarea",
                    with_methods=True,
                )
                checkval = df.iloc[0].aa_textLength / df.iloc[1].aa_textLength > 0.5
                results.append(df.aa_value.iloc[1])
            except Exception:
                sleep(1)
                continue
    driver.close()
    driver.quit()
    return results


text = r"""
Python. was created in the early 1990s by Guido van Rossum at Stichting Mathematisch 
Centrum (CWI, see https://www.cwi.nl/) in the Netherlands as a successor of a 
language called ABC. Guido remains Python’s principal author, although it includes
many contributions from others.
In 1995, Guido. continued his work on Python at the Corporation for 
National Research Initiatives 
(CNRI, see https://www.cnri.reston.va.us/) in Reston, 
Virginia where he released several versions of the software.
""".strip()
#
text_translated = translate(text, langsrc="en", langdst="pt")
print(text_translated)
