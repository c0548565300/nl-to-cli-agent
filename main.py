from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
import gradio as gr

# יוצרים client למודל
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a generator of Windows CMD commands only.
Your task is to receive a natural-language instruction and return exactly one CMD command.

STRICT RULES:

1.You must return one single line only.

2.Do not explain, describe, apologize, or add any extra text.

3.Do not use any formatting:

no backticks

no ```

no code blocks

no markdown

no syntax highlighting

4.Do not output quotes around the command.

5.Do not use PowerShell, Bash, or any other shell — CMD only.

6.Do not add pipes (|), filters, or ANY extra arguments unless the user explicitly requests them.

7.Do not use environment variables (like %USERPROFILE%) unless the user specifically asks.

8.Do not optimize, improve, or enrich the command.

9.Do not change directories. Always assume you are already in the correct working folder unless the user clearly instructs otherwise.

10.The output must always be the simplest and shortest valid CMD command that satisfies the user's instruction.

11.You must NEVER output markdown of any kind.

12.You must output ONLY the raw command, plain text, with no surrounding characters.

13.If the user writes something that cannot be converted into a valid Windows CMD command,
you must NOT guess a command.
Instead, you must reply exactly with this sentence (and nothing else):
Sorry, my role is to convert text into terminal commands only, nothing beyond that.

14.“No flags or parameters unless the user explicitly requests them”

15.If the user's instruction requires running a dangerous or destructive command
(such as: del, erase, rd /s, rm, rm -rf, format, shutdown, diskpart, bcdedit, or any command that can delete files, wipe drives, stop the system, or damage data),
you must NOT output the command.

Instead, you must output exactly the following sentence:

"This command is dangerous and cannot be executed."

No explanations, no extra text, no formatting, no alternatives.

FORMAT REQUIREMENT:
Your output must always be one CMD command only, with no extra text, no formatting, no explanations, and no decorations.
"""

def nl_to_cli(user_instruction: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\nInstruction: {user_instruction}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    # מבנה התשובה החדש
    command = response.output_text.strip()
    return command


# Gradio interface
def gradio_interface(user_instruction: str) -> str:
    """
    פונקציה ש-Gradio יקרא לה.
    """
    if not user_instruction.strip():
        return ""
    return nl_to_cli(user_instruction)

with gr.Blocks(
    title="Natural Language to CLI Agent",
    css="""
    .gradio-container { 
        background: #f7f9fc; 
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #2a4d7a;
        text-align: center;
        font-size: 32px !important;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #4b6584;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .input-box textarea, .output-box textarea {
        border-radius: 12px !important;
        border: 1px solid #a9bcd0 !important;
        padding: 12px !important;
        font-size: 18px !important;
        background: white;
    }

    .output-box textarea {
        background: #eef2f7 !important;
        color: #0a3d62 !important;
        height: auto !important;
    }

    .gr-button {
        background: #2e86de !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        padding: 10px 20px !important;
        border: none !important;
    }

    .gr-button:hover {
        background: #1e6fbe !important;
    }
    """
) as demo:

    gr.HTML("<h1>🧠 Natural Language → 💻 CLI Command</h1>")
    gr.HTML("<div class='subtitle'>כתבי הוראה בשפה טבעית, וה-agent יהפוך אותה לפקודת טרמינל.</div>")

    with gr.Column():
        input_box = gr.Textbox(
           label="הוראה בשפה טבעית",
           placeholder="לדוגמה: מה כתובת ה-IP של המחשב שלי?",
           elem_classes=["input-box"],
           lines=1          # ← קריטי כדי ש-Enter יעבוד!
        )


        run_button = gr.Button("המר לפקודה")

        output_box = gr.Textbox(
            label="פקודת CLI",
            interactive=False,
            elem_classes=["output-box"],
            lines=1
        )

        copy_button = gr.Button("📋 העתק פלט")

    # הפעלה על Enter
    input_box.submit(
        fn=gradio_interface,
        inputs=input_box,
        outputs=output_box
    )

    # הפעלה על לחיצה
    run_button.click(
        fn=gradio_interface,
        inputs=input_box,
        outputs=output_box
    )

    # כפתור העתקה
    copy_button.click(
        fn=lambda text: text,
        inputs=output_box,
        outputs=output_box,
        js="(text) => {navigator.clipboard.writeText(text); alert('הועתק!'); return text;}"
    )


if __name__ == "__main__":
    demo.launch()