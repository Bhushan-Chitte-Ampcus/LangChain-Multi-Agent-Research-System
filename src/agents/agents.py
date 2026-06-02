from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

# Model Initialization
llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    temperature=0.7,
    api_key=os.getenv("LLM_API_KEY")
)

class SimpleAgent:
    """Simple agent that manually handles tool calls."""
    
    def __init__(self, tools, system_prompt):
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = system_prompt
        self.llm = llm
        
    def invoke(self, input_dict):
        """Execute the agent with the given input."""
        user_message = input_dict.get("input", "")
        
        # Build tool descriptions for the prompt
        tool_descriptions = "\n\n".join([
            f"Tool: {name}\nDescription: {tool.description}\nArguments: {json.dumps(tool.args, indent=2)}"
            for name, tool in self.tools.items()
        ])
        
        # Create enhanced system prompt with tools
        enhanced_system = f"""{self.system_prompt}

You have access to the following tools:

{tool_descriptions}

When you need to use a tool, respond with EXACTLY this format:
<TOOL_CALL>
tool_name: <tool_name>
parameters: {{"param1": "value1", "param2": "value2"}}
</TOOL_CALL>

After using a tool, provide your final answer."""
        
        messages = [
            {"role": "system", "content": enhanced_system},
            {"role": "user", "content": user_message}
        ]
        
        # Get response from model
        response = self.llm.invoke(messages)
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Check if response contains a tool call
        tool_call_match = re.search(r'<TOOL_CALL>\s*tool_name:\s*(\w+)\s*parameters:\s*(\{.*?\})\s*</TOOL_CALL>', response_text, re.DOTALL)
        
        if tool_call_match:
            tool_name = tool_call_match.group(1)
            params_str = tool_call_match.group(2)
            
            try:
                params = json.loads(params_str)
                
                if tool_name in self.tools:
                    # Execute tool
                    tool_result = self.tools[tool_name].invoke(params)
                    
                    # Feed result back to model for final response
                    messages.append({"role": "assistant", "content": response_text})
                    messages.append({
                        "role": "user",
                        "content": f"Tool '{tool_name}' returned the following result:\n\n{tool_result}\n\nNow provide your final answer based on this information."
                    })
                    
                    final_response = self.llm.invoke(messages)
                    return {"output": final_response.content if hasattr(final_response, 'content') else str(final_response)}
            except json.JSONDecodeError:
                pass
        
        # Return the response as-is if no tool call or error
        return {"output": response_text}

# Search Agent
def build_search_agent():
    return SimpleAgent(
        tools=[web_search],
        system_prompt="You are a research assistant. Search for recent and reliable information about the user's query using the web_search tool."
    )

# Reader Agent
def build_reader_agent():
    return SimpleAgent(
        tools=[scrape_url],
        system_prompt="You are a web scraper. Extract relevant content from URLs provided to you using the scrape_url tool."
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. write clear, structured and insightful reports."),
    ("human", """
        Write a detailed research report on the topic below.
        Topic: {topic}
        Research Gathered: {research}

        Structure the report as:
        - Introduction
        - Key Findings (minimum 3 well-explained points)
        - Conclusion
        - Sources (list all URLs found in the research)

        Be detailed, factual and professional.
    """)
    ])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """
        Review the research report below and evaluate it strictly.
        Report: {report}
        
        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...
     
        Area to Improve:
        - ...
        - ...
     
        One line verdict:
        - ...
    """)
    ])

critic_chain = critic_prompt | llm | StrOutputParser()