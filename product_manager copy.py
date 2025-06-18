import os
import chardet
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


class Product_Manager(Role):
    name: str = "Pole"
    profile: str = "Product Manager"
    team: Team = None
    llm: object
    llm_sample: object
    system_msg: str = WRITE_PRD_SYS
    own_message: Message = None
    action: str = "functional requirement document"

    def go(self):
        print(self.profile + " " + self.name + " generate PRD......")
        Team.log.info(self.profile + " " + self.name + " Writing PRD...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content

        # ---------- constructing prompt to LLM ----------
        system_prompt = SystemMessage(content=WRITE_PRD_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PRD)
        user_prompt_msg = user_prompt_template.invoke(
            {"original_requirement": original_requirement}
        )

        # prompt LLM
        user_prompt_msg = user_prompt_template.invoke(
            {"original_requirement": original_requirement}
        )
        L_result = self.llm.invoke(system_prompt, user_prompt)
        result = self.llm_sample.invoke(system_prompt, user_prompt)

        # ---------- logging -----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info("\n\n" + LLM_result)

        # ---------- adding result to SCR(before align) ----------
        prd_msg = Message(sender=self.profile, content=LLM_result)
        self.own_message = prd_msg

        Team.all_messages.append(prd_msg)
        # ---------- writing result to local ----------
        self.message_to_file(prd_msg.content)

        return

    def test_code():
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log2.info(system_prompt.content + "\n" + user_prompt.content)

        result2 = self.llm_sample.invoke(system_prompt, user_prompt)
