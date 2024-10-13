# local-llm-structured-output
ローカルLLMでOpenAIが提供するStructured Outputsのような機能を実現するためのサンプル

## 環境構築
### ライブラリダウンロード
* `pip install -r requirements.txt`
* 使用ライブラリ
    ```python
    from pydantic import BaseModel, Field
    from enum import Enum, auto
    from llama_cpp import Llama
    from jinja2 import Template
    from guardrails import Guard, ValidationOutcome    
    ```
### LLMモデルダウンロード
* `gemma-2-2b-jpn-it-IQ4_XS.gguf` を `models/`以下にダウンロード
  * [google/gemma-2-2b-jpn-it](https://huggingface.co/google/gemma-2-2b-jpn-it)を4bit量子化したモデル
  * ダウンロード: [alfredplpl/gemma-2-2b-jpn-it-gguf](https://huggingface.co/alfredplpl/gemma-2-2b-jpn-it-gguf)

## 実行方法
* `python main.py`
  * `times=3` の値を変えることによって生成数を変更可能   

## 実行結果例
```txt
0 name='アリス' weapon=<Weapon.Sword: 'Sword'> description='敏捷な動きと鋭い剣技を持つ。常に敵を倒すために準備を万端にして行動する。'
1 name='アリス' weapon=<Weapon.Sword: 'Sword'> description='明るく元気で、正義感を熱く持ち、勇敢な戦士です。  '
2 name='アキオ' weapon=<Weapon.Staff: 'Staff'> description='不思議な力を持つ、静かな存在。長い時間をかけて鍛えられた杖を使い、周囲の気を操る。その力によって、敵の動きを遅らせることができる。'
... 省略 ...
28 name='アリス' weapon=<Weapon.Sword: 'Sword'> description='勇敢で繊細な心を持つ、剣使い。敵を倒すために、冷静かつ正確な剣術で戦う。 '
index=30
{
      "name": "アリス",
      "weapon": "Sword",
      "description": "明るく笑顔で、時に少し無邪気な性格。強い剣使いであり、人を助けるために戦い続ける。」
    }
validated_output.error='Unterminated string starting at: line 4 column 22 (char 69)'
--------------
30 name='アリス' weapon=<Weapon.Staff: 'Staff'> description='静かな場所で魔法を唱えるのが得意。不思議な力と冷静さを兼ね備えた人物。'
...
```