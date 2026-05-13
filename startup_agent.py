from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.chains.sequential import SequentialChain

# Load API Key
load_dotenv()

# AI Model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9
)

# -----------------------------
# CHAIN 1 — Startup Idea
# -----------------------------

idea_prompt = PromptTemplate(
    input_variables=["industry", "audience"],
    template="""
    Generate a unique startup idea.

    Industry: {industry}
    Target Audience: {audience}

    Startup Idea:
    """
)

idea_chain = LLMChain(
    llm=llm,
    prompt=idea_prompt,
    output_key="startup_idea"
)

# -----------------------------
# CHAIN 2 — Business Name
# -----------------------------

name_prompt = PromptTemplate(
    input_variables=["startup_idea"],
    template="""
    Create a catchy startup name for this idea:

    {startup_idea}

    Business Name:
    """
)

name_chain = LLMChain(
    llm=llm,
    prompt=name_prompt,
    output_key="business_name"
)

# -----------------------------
# CHAIN 3 — Tagline
# -----------------------------

tagline_prompt = PromptTemplate(
    input_variables=["business_name"],
    template="""
    Create a short catchy tagline for:

    {business_name}

    Tagline:
    """
)

tagline_chain = LLMChain(
    llm=llm,
    prompt=tagline_prompt,
    output_key="tagline"
)

# -----------------------------
# CHAIN 4 — Marketing Pitch
# -----------------------------

pitch_prompt = PromptTemplate(
    input_variables=[
        "startup_idea",
        "business_name",
        "tagline"
    ],
    template="""
    Create a short marketing pitch.

    Startup Idea:
    {startup_idea}

    Business Name:
    {business_name}

    Tagline:
    {tagline}

    Marketing Pitch:
    """
)

pitch_chain = LLMChain(
    llm=llm,
    prompt=pitch_prompt,
    output_key="marketing_pitch"
)

# -----------------------------
# SEQUENTIAL CHAIN
# -----------------------------

final_chain = SequentialChain(
    chains=[
        idea_chain,
        name_chain,
        tagline_chain,
        pitch_chain
    ],

    input_variables=[
        "industry",
        "audience"
    ],

    output_variables=[
        "startup_idea",
        "business_name",
        "tagline",
        "marketing_pitch"
    ],

    verbose=True
)

# -----------------------------
# USER INPUT
# -----------------------------

industry = input("Enter Industry: ")
audience = input("Enter Target Audience: ")

# Run Chain
result = final_chain({
    "industry": industry,
    "audience": audience
})

# -----------------------------
# OUTPUT
# -----------------------------

print("\n🚀 STARTUP IDEA")
print(result["startup_idea"])

print("\n🏢 BUSINESS NAME")
print(result["business_name"])

print("\n✨ TAGLINE")
print(result["tagline"])

print("\n📢 MARKETING PITCH")
print(result["marketing_pitch"])