from enum import Enum
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import Field, BaseModel, validator

from app.settings import get_openai_api_key


class SentenceFix(BaseModel):
    original_sentence: str = Field(description="Original sentence intended by the user.")
    spoken_sentence: str = Field(description="Sentence as spoken by the user.")
    feedback: str = Field(description="Suggestions for improvement based on sentence comparison.")
    fix: str = Field(description="Type of discrepancy between original and spoken sentences. [match, different, missed]")


class SlideFeedback(BaseModel):
    slide_image_description: str = Field(description="Description of slide's visual content.")
    slide_content_sentences: List[SentenceFix] = Field(description="List of original sentence with spoken sentence for discrepancy analysis and feedback.")


feedback_template = """
Task Overview:
You are an API designed to compare two scripts: original_script and spoken_script. The original_script is the user-defined script that was intended to be spoken during a presentation, while the spoken_script is what the user actually said during the presentation.

Your Responsibilities:
Comparing Scripts: Analyze the original_script and spoken_script to identify discrepancies.
Generate Feedback: add feedback based on original srcipt so that user can improve their speaking in real presentation short in korean.
Response Language: you response and feedback language must be written language

Types of Discrepancies to Identify:
Match Content
- Exact alignment in both wording and context, without any variations.
- All key keywords and the core message must be fully preserved.

Different Content
- Any deviation from the original script, including minor alterations in wording or omission of any key keywords.

Missed Content
- Original sentences or key ideas absent in the spoken script.

Output Format
{format_instructions}

Original Script
{original_script}

Spoken Script
{spoken_script}
"""

# model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
model = ChatOpenAI(api_key=get_openai_api_key(), temperature=0)

parser = PydanticOutputParser(pydantic_object=SlideFeedback)

prompt = PromptTemplate(
    template=feedback_template,
    input_variables=["original_script", "spoken_script"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model | parser

if __name__ == "__main__":

    original_script = """
    오전의 대표기능 4가지를 소개하겠습니다
    홈에서는 공예, 국악, 무용, 고궁 등 장르별로 행사, 전시, 축제, 공연과 같은 정보를 제공하고
    주변탐색을 통해 가장 가까운 전통문화 콘텐츠를 발견할 수 있습니다
    마음에 드는 콘텐츠를 발견하면
    이용정보 뿐아니라, 후기확인과 예약까지도 진행할 수 있는데요
    현재는 예약버튼을 누르면 타사의 예약앱으로 이동하지만,
    추후 앱 내에서의 예약 기능을 업데이트할 예정입니다
    """

    spoken_script = """
    안녕하세요, 여러분. 오늘 저는 오전의 주요 기능 네 가지에 대해 소개하고자 합니다. 
    첫 번째로, 홈 화면에서는 다양한 장르별 행사 정보를 제공합니다. 
    여기에는 공예, 국악, 무용, 고궁과 관련된 전시, 축제, 공연 정보가 포함됩니다. 
    주변탐색을 통해 가장 가까운 전통문화 콘텐츠를 발견할 수 있습니다
    세 번째로, 마음에 드는 콘텐츠를 찾게 되면 이용 정보뿐만 아니라, 후기 확인과 예약도 가능합니다. 
    마지막으로, 현재 예약 버튼을 누르면 다른 예약 앱으로 연결되지만, 앞으로 앱 내에서 바로 예약할 수 있는 기능을 업데이트할 계획입니다. 
    이 모든 기능들은 사용자가 전통문화에 쉽게 접근하고 즐길 수 있도록 도와줄 것입니다.
    """

    feedback = chain.invoke({"original_script": original_script, "spoken_script": spoken_script})
