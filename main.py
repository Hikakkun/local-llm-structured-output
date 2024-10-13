from pydantic import BaseModel, Field
from enum import Enum, auto
from llama_cpp import Llama
from jinja2 import Template
from guardrails import Guard, ValidationOutcome


class Weapon(Enum):
    def _generate_next_value_(name, start, count, last_values):
        """
        Enumメンバーの自動生成時に呼び出されるメソッド。

        Args:
            name (str): 新しく生成されるEnumメンバーの名前。
            start (int): 初期化時に指定された値（最初のメンバーにのみ適用）。
            count (int): 現在までに生成されたEnumメンバーの数。
            last_values (list): これまでに生成されたすべてのEnumメンバーの値のリスト。

        Returns:
            str: Enumメンバーの値として使用される名前（今回はそのまま文字列として使用）。
        """
        return name

    # 武器の種類を定義
    Staff = auto()
    Sword = auto()
    Bow = auto()
    FryingPan = auto()
    DualBlades = auto()
    Gun = auto()


class Character(BaseModel):
    # キャラクターの基本情報を定義
    name: str = Field(
        description="キャラクターの名前",
    )
    weapon: Weapon = Field(
        description="キャラクターが使用する武器の種類",
    )
    description: str = Field(
        description="キャラクター得意技などのキャラクターを体現するような説明",
    )


def create_prompt(prompt: str, system_prompt: str | None = None) -> str:
    """
    ユーザーの入力とシステムプロンプトをテンプレートとして結合し、LLMに送信するプロンプトを作成する。

    Args:
        prompt (str): ユーザーからの入力。
        system_prompt (str | None): システムプロンプト（オプション）。

    Returns:
        str: LLMに送信するためのプロンプト。
    """
    # Jinjaテンプレートを定義
    template_str = """
<start_of_turn>user
{% if system_prompt %}{{ system_prompt }} {% endif %}{{ prompt }}<end_of_turn>
<start_of_turn>model
<end_of_turn>
    """

    # テンプレートをコンパイル
    template = Template(template_str)

    # テンプレートにデータを渡してレンダリング
    return template.render(system_prompt=system_prompt, prompt=prompt)


# LLMに送信するシステムプロンプトを定義
system_prompt = f"""出力は次のJSON Schemaに準拠し、Json形式で行うこと。
```json
{Character.model_json_schema()}
```
"""

# ユーザープロンプト
prompt = "キャラクターを生成して"

# GuardrailsでCharacterのスキーマを検証
guard = Guard.for_pydantic(Character)

# Llamaモデルのロード
llm = Llama(model_path="gemma-2-2b-jpn-it-IQ4_XS.gguf", n_ctx=1024, verbose=False)

times = 3
for index in range(times):
    # LLMからの出力を生成
    output = llm(
        create_prompt(prompt, system_prompt), max_tokens=1000, temperature=0.99
    )
    json_str = output["choices"][0]["text"]
    # Guardrailsで出力を検証
    validated_output: ValidationOutcome = guard.parse(json_str)
    if not validated_output.validation_passed:
        # 検証に失敗した場合の処理
        print(f"index={index+1}")
        print(json_str.strip())
        print(f"{validated_output.error=}")
        print("--------------")
    else:
        # 検証に成功した場合の処理
        print(index, Character(**validated_output.validated_output))
