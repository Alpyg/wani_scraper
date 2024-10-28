import argparse
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

from utils import COLOR, get_level_difficulty
import kanji
import vocabulary


def main():
    parser = argparse.ArgumentParser(
        prog="wani_scraper",
        description="Scrapes WaniKani for all Radicals, Kanji and Vocabulary",
    )
    parser.add_argument("type", choices=["kanji", "vocabulary"])

    args = parser.parse_args()
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    for level in range(1, 61):
        driver.get(
            f"https://wanikani.com/{args.type}?difficulty={get_level_difficulty(level)}"
        )

        # Scrape urls
        section = driver.find_element(By.XPATH, f"//section[.//a[@id='level-{level}']]")
        anchors = section.find_elements(By.XPATH, ".//div//ol//li//a")
        urls = [anchor.get_attribute("href") for anchor in anchors]

        for url in urls:
            driver.get(url)
            match args.type:
                case "kanji":
                    data = [
                        "WaniKani::Kanji",
                        "WaniKani Kanji",
                        f"kanji level{level:02}",
                        kanji.extract_kanji(driver),
                        kanji.extract_meaning(driver),
                        kanji.extract_radicals(driver),
                        *kanji.extract_readings(driver),
                        *kanji.extract_mnemonic(driver, "meaning"),
                        *kanji.extract_mnemonic(driver, "reading"),
                    ]
                    print("\t".join(data))

                case "vocabulary":
                    data = [
                        "WaniKani::Vocabulary",
                        "WaniKani Vocabulary",
                        f"vocabulary level{level:02}",
                        vocabulary.extract_vocabulary(driver),
                        *vocabulary.extract_meaning(driver),
                        vocabulary.extract_reading(driver),
                        vocabulary.extract_explanation(driver, "meaning"),
                        vocabulary.extract_explanation(driver, "reading"),
                        vocabulary.extract_context_sentences(driver),
                    ]
                    print("\t".join(data))

            time.sleep(0.1)

        time.sleep(1)

    driver.quit()


if __name__ == "__main__":
    main()
