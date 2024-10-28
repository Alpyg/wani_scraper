from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils import annotate, COLOR


def extract_vocabulary(driver):
    return driver.find_element(
        By.XPATH, "//span[@class='page-header__icon page-header__icon--vocabulary']"
    ).text


def extract_meaning(driver):
    primary_meaning = driver.find_element(
        By.XPATH, "//h2[contains(text(), 'Primary')]/following-sibling::p"
    ).text
    try:
        alternatives = driver.find_element(
            By.XPATH, "//h2[contains(text(), 'Alternative')]/following-sibling::p"
        ).text
    except NoSuchElementException:
        alternatives = None

    word_type = driver.find_element(
        By.XPATH, "//h2[contains(text(), 'Word Type')]/following-sibling::p"
    ).text

    return (
        ", ".join(
            [
                item
                for item in [f"<b>{primary_meaning}</b>", alternatives]
                if item is not None
            ]
        ),
        word_type,
    )


def extract_reading(driver):
    reading_element = driver.find_element(
        By.XPATH, "//section[@id='section-reading']//div[@lang='ja']"
    )

    # TODO: Audio

    return reading_element.text


def extract_explanation(driver, section):
    explanation_elements = driver.find_elements(
        By.XPATH,
        f"//section[@id='section-{section}']//h3[contains(text(), 'Explanation')]/following-sibling::p",
    )

    explanation = "<br>".join(
        [annotate(p.get_attribute("innerHTML").strip()) for p in explanation_elements]
    ).replace("\n", "")

    return explanation


def extract_context_sentences(driver):
    sentences_elements = driver.find_elements(
        By.XPATH, "//h3[contains(text(), 'Context Sentences')]/following-sibling::div"
    )

    return "<br><br>".join(
        "<br>".join(p.text for p in div.find_elements(By.TAG_NAME, "p"))
        for div in sentences_elements
    )
