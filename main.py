import random
import streamlit as st
from prompt_gen import PromptGenerator, PromptGeneratorConfig

from templates import templates


class AISalesPromptCreator:
    def __init__(self):
        self.templates = templates

        self.selected_template = (
            "SaaS Productivity Software"  # Automatically load this template on start
        )
        self.api_key = ""
        self.ai_name = ""
        self.base_url = ""
        self.industry = ""
        self.company_name = ""
        self.target_audience = ""
        self.product_description = ""
        self.challenges_solved = ""
        self.call_objective = ""
        self.common_objections = ""
        self.additional_context = ""

    def load_template(self, template_name):
        template = self.templates.get(template_name, self.templates["Default"])
        self.ai_name = template["ai_name"]
        self.industry = template["industry"]
        self.company_name = template["company_name"]
        self.target_audience = template["target_audience"]
        self.product_description = template["product_description"]
        self.challenges_solved = template["challenges_solved"]
        self.call_objective = template["call_objective"]
        self.common_objections = template["common_objections"]
        self.additional_context = template["additional_context"]

    def render_api_keys(self):
        with st.expander("LLM Settings", expanded=True):
            self.llm_model = st.text_input(
                "Model Name", placeholder="ollama/llama3.1", value="ollama/llama3.1"
            )
            self.api_key = st.text_input("API Key", placeholder="sk-...", value="N/A")
            self.base_url = st.text_input(
                "Base URL",
                placeholder="http://localhost:11434",
                value="http://localhost:11434",
            )

    def render_templates(self):
        st.subheader("Templates")
        self.selected_template = st.selectbox(
            "Select a Template", list(self.templates.keys())
        )
        if st.button("Load Template"):
            self.load_template(self.selected_template)

    def render_inputs(self):
        col1, col2 = st.columns(2)

        with col1:
            self.ai_name = st.text_input(
                "AI Representative Name", value=self.ai_name, placeholder="e.g. Sarah"
            )
            self.industry = st.text_input(
                "Industry", value=self.industry, placeholder="e.g. SaaS, Healthcare"
            )

        with col2:
            self.company_name = st.text_input(
                "Company Name",
                value=self.company_name,
                placeholder="e.g. TechCorp Solutions",
            )
            self.target_audience = st.text_input(
                "Target Audience",
                value=self.target_audience,
                placeholder="e.g. Small business owners",
            )

        self.product_description = st.text_area(
            "Product/Service Description",
            value=self.product_description,
            placeholder="Describe your product or service and its key features...",
        )

        self.challenges_solved = st.text_area(
            "Challenges Solved",
            value=self.challenges_solved,
            placeholder="What specific problems does your product solve?",
        )

        self.call_objective = st.text_input(
            "Call Objective",
            value=self.call_objective,
            placeholder="e.g. Schedule a demo, Book a consultation",
        )

        self.common_objections = st.text_area(
            "Common Objections",
            value=self.common_objections,
            placeholder="List the most common objections and how to handle them...",
        )

        self.additional_context = st.text_area(
            "Additional Context (Optional)",
            value=self.additional_context,
            placeholder="Add any additional details that might be helpful...",
        )

    def render_buttons(self):
        col1, col2 = st.columns([6, 1], vertical_alignment="center")

        with col1:
            if st.button("Generate", use_container_width=True):
                self.generate_prompt()

        with col2:
            if st.button("Reset"):
                self.reset_fields()

    def generate_prompt(self):
        gen = PromptGenerator(
            PromptGeneratorConfig(
                api_key=self.api_key,
                model=self.llm_model,
                api_base=self.base_url,
                # AI options
                industry=self.industry,
                company_name=self.company_name,
                target_audience=self.target_audience,
                product_description=self.product_description,
                challenges_solved=self.challenges_solved,
                call_objective=self.call_objective,
                common_objections=self.common_objections,
                additional_context=self.additional_context,
                ai_name=self.ai_name,
            )
        )

        prompt = gen.generate_prompt(stream=True)
        st.session_state["generated_prompt"] = prompt

    def reset_fields(self):
        self.load_template("Default")
        st.session_state["generated_prompt"] = ""

    def render_generated_prompt(self):
        st.divider()
        st.subheader("Generated Prompt")
        text_generator = st.session_state.get("generated_prompt", "")
        text_area = st.empty()

        t = ""
        for text in text_generator:
            t += text
            text_area.text_area(
                key=str(random.sample(range(100), 10)),
                label="Copy and test your prompt",
                value=t,
                height=500,
                disabled=True,
            )

    def render_footer(self):
        st.divider()
        st.markdown(
            "<div style='text-align: center; color: gray; font-size: small;'>"
            "A glimpse of what's possible, powered by Navicstein Chinemerem Voice AI Solutions"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align: center;'>"
            "<a href='https://www.linkedin.com/in/navicstein' style='margin: 0 10px;'>LinkedIn</a>"
            "<a href='https://github.com/steinathan' style='margin: 0 10px;'>GitHub</a>"
            "</div>",
            unsafe_allow_html=True,
        )

    def run(self):
        st.title("AI Prompt Creator, Sales?")
        st.subheader("Generate personalized AI representative prompts in seconds")

        self.render_api_keys()
        self.render_templates()
        self.load_template(self.selected_template)  # Auto-load the default template
        self.render_inputs()
        self.render_buttons()
        self.render_generated_prompt()
        self.render_footer()


if __name__ == "__main__":
    if "generated_prompt" not in st.session_state:
        st.session_state["generated_prompt"] = ""

    app = AISalesPromptCreator()
    app.run()
