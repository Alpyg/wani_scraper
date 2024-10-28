from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils import annotate, COLOR


def extract_kanji(driver):
    return driver.find_element(
        By.XPATH, "//span[@class='page-header__icon page-header__icon--kanji']"
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
    return ", ".join(
        [
            item
            for item in [f"<b>{primary_meaning}</b>", alternatives]
            if item is not None
        ]
    )


def extract_radicals(driver):
    radical_elements = driver.find_elements(
        By.XPATH,
        "//section[@id='section-components']//li[@class='subject-list__item']",
    )

    radicals = []
    for radical in radical_elements:
        character = radical.find_element(
            By.CSS_SELECTOR, ".subject-character__characters"
        )

        children = character.find_elements(By.XPATH, "./*")
        if len(children) > 0:
            character = (
                f'<img src="{children[0].get_attribute("src")}" class="radical">'
            )
        else:
            character = character.text

        meaning = radical.find_element(
            By.CSS_SELECTOR, ".subject-character__meaning"
        ).text
        radicals.append(
            f'<font color="{COLOR["radical"]}">{character}</font> {meaning}'
        )
    radicals = ", ".join(radicals)

    return radicals


def extract_readings(driver):
    onyomi_element = driver.find_element(
        By.XPATH, "//h3[contains(text(), 'On’yomi')]/following-sibling::p"
    )
    kunyomi_element = driver.find_element(
        By.XPATH, "//h3[contains(text(), 'Kun’yomi')]/following-sibling::p"
    )

    onyomi_parent = onyomi_element.find_element(By.XPATH, "./parent::*")
    kunyomi_parent = kunyomi_element.find_element(By.XPATH, "./parent::*")

    onyomi = (
        f"<b>{onyomi_element.text}</b>"
        if onyomi_parent.value_of_css_property("opacity") == "1"
        else onyomi_element.text
    )
    kunyomi = (
        f"<b>{kunyomi_element.text}</b>"
        if kunyomi_parent.value_of_css_property("opacity") == "1"
        else kunyomi_element.text
    )

    return onyomi, kunyomi


def extract_mnemonic(driver, target):
    mnemonic_element = driver.find_element(
        By.XPATH,
        f"//section[@class='subject-section subject-section--{target}']//h3[contains(text(), 'Mnemonic')]/following-sibling::p",
    )
    if mnemonic_element is None:
        return "", ""

    mnemonic = annotate(mnemonic_element.get_attribute("innerHTML"))

    hint_elements = driver.find_elements(
        By.XPATH,
        f"//section[@class='subject-section subject-section--{target}']//h3[contains(text(), 'Mnemonic')]/following-sibling::aside",
    )

    if hint_elements:
        hint_element = hint_elements[0]
        hint = "<br>".join(
            [
                annotate(p.get_attribute("innerHTML").strip())
                for p in hint_element.find_elements(By.TAG_NAME, "p")
            ]
        )
    else:
        hint = ""

    return mnemonic, hint
