from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Expectation:
    sub_title: str
    sub_expectations: list[str]


@dataclass
class ParcourSupExpectations:
    title: str
    expectations: list[Expectation]


class HtmlParser:
    PARSER = "html.parser"

    HTML_TITLE_TAG = ["h1", "h5"]
    HTML_EXPECTATION_TAG = ["p", "li"]
    HTML_MAIN_EXPECTATION_TAG = "b"

    def __init__(self, html_content: str):
        self.__expectations: list[Expectation] = []
        self.__soup: BeautifulSoup = BeautifulSoup(html_content, self.PARSER)

    def _create_main_expectation(self, element_text: str) -> Expectation:
        return Expectation(sub_title=element_text.strip(), sub_expectations=[])

    def _add_sub_expectation(self, current_expectation: Expectation, element_text: str):
        current_expectation.sub_expectations.append(element_text.strip())

    def _process_paragraph_element(self, element, current_expectation: Expectation):
        if current_expectation:
            self._add_sub_expectation(current_expectation, element.text)
        elif paragraph := element.find(self.HTML_EXPECTATION_TAG[0]):
            self.__expectations.append(self._create_main_expectation(paragraph.text))

    def _process_element(
        self, element, current_expectation: Expectation
    ) -> Expectation:
        if bold := element.find(self.HTML_MAIN_EXPECTATION_TAG):
            if current_expectation:
                self.__expectations.append(current_expectation)
            return self._create_main_expectation(bold.text)
        else:
            self._process_paragraph_element(element, current_expectation)
            return current_expectation

    def _extract_expectations(self) -> list[Expectation]:
        current_expectation = None

        for element in self.__soup.find_all(self.HTML_EXPECTATION_TAG):
            current_expectation = self._process_element(element, current_expectation)

        if current_expectation:
            self.__expectations.append(current_expectation)

        return self.__expectations

    def _extract_title(self) -> str:
        return self.__soup.find(self.HTML_TITLE_TAG).text

    def parse_html(self) -> ParcourSupExpectations:
        title = self._extract_title()
        expectations = self._extract_expectations()

        return ParcourSupExpectations(title, expectations)
