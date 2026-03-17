import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import gradio as gr

# טעינת משתני סביבה
load_dotenv()

# יצירת client למודל
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a generator of Windows CMD commands only.
Your task is to receive a natural-language instruction and return exactly one CMD command.

STRICT RULES:
1. You must return one single line only.
2. Do not explain, describe, apologize, or add any extra text.
3. Do not use any formatting (no backticks, no code blocks).
4. Do not output quotes around the command.
5. Use CMD only (not PowerShell).
6. Use the simplest valid command.
7. If the instruction is dangerous (del, format, shutdown, etc.), output exactly: "This command is dangerous and cannot be executed."
8. If the instruction is invalid, output exactly: "Sorry, my role is to convert text into terminal commands only, nothing beyond that."
"""

def nl_to_cli(user_instruction: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Instruction: {user_instruction}"}
            ],
            temperature=0
        )

        command = response.choices[0].message.content.strip()
        return command

    except openai.AuthenticationError:
        return "שגיאה: מפתח ה-API אינו תקין. בדקו את קובץ ה-.env שלכם."
    except openai.RateLimitError:
        return "שגיאה: חרגתם ממכסת השימוש ב-API. נסו שוב מאוחר יותר."
    except Exception as e:
        return f"אופס! קרתה שגיאה לא צפויה: {str(e)}"

def gradio_interface(user_instruction: str) -> str:
    if not user_instruction.strip():
        return ""
    return nl_to_cli(user_instruction)

with gr.Blocks(title="Natural Language to CLI Agent", css="""
    .gradio-container { background: #f7f9fc; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #2a4d7a; text-align: center; font-weight: bold; }
    .subtitle { text-align: center; color: #4b6584; margin-bottom: 25px; }
    .input-box textarea, .output-box textarea { border-radius: 12px !important; font-size: 18px !important; }
    .output-box textarea { background: #eef2f7 !important; color: #0a3d62 !important; }
    .gr-button { background: #2e86de !important; color: white !important; border-radius: 10px !important; }
""") as demo:

    gr.HTML("<h1>🧠 Natural Language → 💻 CLI Command</h1>")
    gr.HTML("<div class='subtitle'>כתבו הוראה בשפה טבעית, וה-agent יהפוך אותה לפקודת טרמינל.</div>")

    with gr.Column():
        input_box = gr.Textbox(
           label="הוראה בשפה טבעית",
           placeholder="לדוגמה: מה כתובת ה-IP של המחשב שלי?",
           lines=1
        )

        run_button = gr.Button("המר לפקודה")

        output_box = gr.Textbox(
            label="פקודת CLI",
            interactive=False,
            lines=1
        )

        copy_button = gr.Button("📋 העתק פלט")

    # הפעלה על Enter ועל לחיצה
    input_box.submit(fn=gradio_interface, inputs=input_box, outputs=output_box)
    run_button.click(fn=gradio_interface, inputs=input_box, outputs=output_box)

    # כפתור העתקה עם JS
    copy_button.click(
        fn=lambda text: text,
        inputs=output_box,
        outputs=output_box,
        js="(text) => { if(text) { navigator.clipboard.writeText(text); alert('הועתק!'); } return text; }"
    )

if __name__ == "__main__":
    demo.launch()