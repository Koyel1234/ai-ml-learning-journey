Parameters of ChatModels:<br><br>
**Temperature:**

`temperature` is a parameter that controls the randomness of a language model's output. It affects how creative or deterministic the responses are.
- Lower Values (`0.0 - 0.3`) -> More deterministic and predictable.
- Higher Values (`0.7 - 1.5`) -> More random, creative and diverse.

<div align='center'>
<table>
<tr><th>Use Case</th><th>Recommended Temperature</th></tr>
<tr><td>Factual Answers (math, code, facts)</td><td><kbd>0.0 - 0.3</kbd></td></tr>
<tr><td>Balanced Response (general QA, expalnations)</td><td><kbd>0.5 - 0.7</kbd></td></tr>
<tr><td>creative writing, storytelling, jokes</td><td><kbd>0.9 - 1.2</kbd></td></tr>
<tr><td>Maximum randomness (wild ideas, brainstorming)</td><td><kbd>1.5+</kbd></td></tr>
</table>
</div>
<br><br>

**max_completion_tokens:**

- This allows to select maximum numbers of tokens to show in output.
- This parameter is important because user has to pay as per udsage, so as developper I can restrict this to manage costing.

## Document Similarity Search
This is RAG fundamental.


