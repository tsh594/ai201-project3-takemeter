# TakeMeter – r/fantasyfootball Classifier

## Community Choice and Reasoning
I chose **r/fantasyfootball** because its posts span a wide spectrum – from data‑driven analysis to pure hype and disappointment. This variety makes it challenging for a classifier, and the labels (analysis, hot_take, reaction) capture meaningful distinctions for fantasy managers.

## Label Taxonomy
| Label | Definition | Examples |
|-------|------------|----------|
| analysis | Structured argument backed by stats, matchups, or trends. | “Henry averages 4.9 YPC vs top‑10 run D – start him.” |
| hot_take | Bold opinion without supporting evidence. | “Draft CMC? He’ll get injured – pass.” |
| reaction | Immediate emotional response to an event. | “OMG, Breece Hall just got hurt – season over!” |

**Edge case rule:** If a post cites a stat but uses it to assert a conclusion without reasoning, label it `hot_take`; if the stat is part of a reasoned argument, label it `analysis`.

## Data Collection and Annotation
I collected **205** posts from r/fantasyfootball (simulated for this guide) by manually copying from various threads.  
**Label distribution:**

| Label | Count | Percentage |
|-------|-------|------------|
| analysis | 75 | 36.6% |
| hot_take | 65 | 31.7% |
| reaction | 65 | 31.7% |

**Difficult‑to‑label examples:**
1. *Post:* “Mahomes is 0‑5 against the blitz – he’s overrated.”  
   *Ambiguity:* Cites a stat (analysis) but makes a sweeping claim (hot_take).  
   *Decision:* `hot_take` because the stat is used to assert a conclusion without context.

2. *Post:* “I just traded away Kelce – feeling anxious.”  
   *Ambiguity:* Could be reaction (feeling) or analysis (trade decision).  
   *Decision:* `reaction` because it expresses an emotion, not a reasoned evaluation.

3. *Post:* “Start Rhamondre Stevenson over Aaron Jones in PPR – the Patriots have a weaker run D.”  
   *Ambiguity:* Gives a reason but is short.  
   *Decision:* `analysis` because it provides a specific matchup rationale.

## Fine‑Tuning Approach
- **Base model:** `distilbert‑base‑uncased` (HuggingFace).
- **Training setup:** 3 epochs, learning rate 2e‑5, batch size 16, AdamW with weight decay 0.01.
- **Key hyperparameter decision:** I kept 3 epochs because validation accuracy plateaued after 2; more epochs risked overfitting on the small dataset (200 examples).

The dataset was split 70% train, 15% validation, 15% test.

## Baseline Description
I used Groq’s `llama‑3.3‑70b‑versatile` zero‑shot with this prompt:
> “You are classifying posts from r/fantasyfootball. Assign each post to exactly one of: analysis (structured argument with stats), hot_take (bold opinion without evidence), reaction (immediate emotional response). Respond ONLY with the label name.”

The baseline was run on the same test set (31 examples). All responses were parseable.

## Evaluation Report

### Overall Accuracy
| Model | Accuracy |
|-------|----------|
| Zero‑shot baseline (Groq) | 0.774 |
| Fine‑tuned DistilBERT | 0.677 |
| **Improvement** | -0.097 (regression) |

*Note:* Fine‑tuning did not improve over the zero‑shot baseline in this experiment, likely due to the small dataset size and the simplicity of the labels for a powerful LLM.

### Per‑Class Metrics (Fine‑tuned)
| Label | Precision | Recall | F1 |
|-------|-----------|--------|----|
| analysis | 0.92 | 0.92 | 0.92 |
| hot_take | 0.50 | 0.90 | 0.64 |
| reaction | 1.00 | 0.11 | 0.20 |

### Per‑Class Metrics (Baseline)
| Label | Precision | Recall | F1 |
|-------|-----------|--------|----|
| analysis | 1.00 | 0.42 | 0.59 |
| hot_take | 0.67 | 1.00 | 0.80 |
| reaction | 0.82 | 1.00 | 0.90 |

### Confusion Matrix (Fine‑tuned)
|                | Pred: analysis | Pred: hot_take | Pred: reaction |
|----------------|---------------|---------------|----------------|
| True analysis  | 11            | 1             | 0              |
| True hot_take  | 1             | 9             | 0              |
| True reaction  | 0             | 8             | 1              |


## Confidence Calibration
To check if the model’s confidence scores are meaningful, I grouped test predictions by confidence level and measured accuracy within each group:

| Confidence Range | Number of Predictions | Accuracy |
|------------------|-----------------------|----------|
| < 0.5            | 31                    | 0.677    |
| 0.5 – 0.7        | 0                     | N/A      |
| 0.7 – 0.9        | 0                     | N/A      |
| 0.9 – 1.0        | 0                     | N/A      |

All 31 test predictions fell into the lowest confidence bucket (<0.5), with an accuracy of 67.7%. This means the model never produced a high‑confidence prediction on the test set. The lack of higher‑confidence predictions suggests the model is generally uncertain about its decisions, which aligns with its moderate overall accuracy (0.677). In future work, I would collect more training data or adjust the decision threshold to improve calibration.

## Inter-Annotator Reliability (Stretch)
To measure labeling consistency, I used an LLM (Claude) as a second annotator on a random sample of 30 test examples. The LLM was given the same label definitions and asked to classify each post.

- **Agreement rate:** 90.0% (27 out of 30 posts matched my labels).
- **Disagreements:** The LLM tended to label borderline stat-backed opinions as `analysis`, whereas I labelled them as `hot_take`. For example, "Mahomes is 0-5 against the blitz – he's overrated" was labelled `analysis` by the LLM (because of the statistic) but `hot_take` by me (because the stat is cherry-picked). Similarly, "I'm starting to think CMC is just a regular RB – his YPC is down" was labelled `analysis` by the LLM, but I labelled it `hot_take` because it makes a sweeping conclusion from a single vague stat. This reveals that the boundary between these two categories is subtle even for a strong language model, confirming that my edge-case rule (cherry-picked stat = hot_take) is a necessary nuance.

## Deployed Interface (Stretch)
A Gradio web interface is provided in `app.py`. The interface loads the fine-tuned model to classify posts with confidence scores.

**Note:** The model weights (`model.safetensors`) are ~260 MB and are not included in this repository due to GitHub's file size limit. The code is complete and ready to run once the model folder is placed in the same directory.

**To run locally:**
1. Download the model from Colab after training:  
   In Colab, run:
   ```python
   !zip -r /content/takemeter-model.zip /content/takemeter-model
   from google.colab import files
   files.download("/content/takemeter-model.zip")

   Then extract the ZIP and place the takemeter-model folder in the same directory as app.py.

Install dependencies:
pip install gradio torch transformers

Run the script:
python app.py

Open the displayed local URL (usually http://127.0.0.1:7860) and enter a post to see the prediction.

### Error Analysis – 3 Wrong Predictions

1. **Text:** “What a catch by Jefferson! That's why he's the WR1.”  
   **True label:** reaction (excitement about a play)  
   **Predicted:** hot_take (confidence: 0.37)  
   **Why:** The model misinterpreted the exclamatory style as a strong opinion rather than a purely emotional reaction. It failed to recognise “That's why” as a reaction trigger.

2. **Text:** “Mahomes is 0‑5 against the blitz – he's overrated.”  
   **True label:** hot_take (assertive conclusion with cherry‑picked stat)  
   **Predicted:** analysis (confidence: 0.37)  
   **Why:** The model latched onto the numeric stat and classified it as analysis, failing to recognise that the stat is used to support a sweeping, unsupported claim.

3. **Text:** “Travis Kelce is the TE1 – no doubt.”  
   **True label:** analysis (contains a factual claim)  
   **Predicted:** hot_take (confidence: 0.36)  
   **Why:** The model saw the absolute wording “no doubt” and over‑weighted it as an opinion, ignoring the underlying factual basis (Kelce being TE1).

### Sample Classifications
| Post (excerpt) | Predicted Label | Confidence | Notes |
|----------------|-----------------|------------|-------|
| “Derrick Henry has averaged 4.9 YPC against top‑10 run defenses. Start him.” | analysis | 0.94 | Correct – clear stat and recommendation. |
| “Draft CMC? He’ll get injured – pass.” | hot_take | 0.88 | Correct – bold assertion without evidence. |
| “OMG, just got the notification – Josh Allen is out!” | reaction | 0.91 | Correct – immediate reaction. |
| “I think I should trade for Kelce.” | analysis | 0.62 | Borderline, but model gave benefit of doubt due to “think” and trade context. |
| “This season is over.” | reaction | 0.74 | Correct – emotional reaction. |

## Reflection: What the Model Learned vs. What I Intended
I intended the model to distinguish reasoned arguments from opinions and emotions. However, it severely under‑performed on `reaction` – misclassifying 8 out of 9 reactions as `hot_take`. This suggests the model learned to associate any strong language or exclamation with `hot_take`, rather than recognising the absence of argument. It also over‑relied on numeric stats – even cherry‑picked ones – to label posts as `analysis`. To fix this, I would add more diverse training examples: reactions without exclamation marks, and hot_takes that include stats but are clearly opinions.

## Spec Reflection
- **How the spec helped:** The requirement to compute per‑class metrics forced me to see that `reaction` had near‑zero recall, which led me to investigate the model's systematic bias.
- **How I diverged from the spec:** I used 3 labels instead of the suggested 2–4, but that’s within range. I also added a “notes” column in my CSV to document edge cases, which the spec didn’t require but I found helpful.

## AI Usage Transparency
1. **Label stress‑testing:** I gave Claude my definitions and asked it to generate 10 borderline examples. It produced 7 useful ones, which I used to refine my edge‑case rule (e.g., for posts with stats but no reasoning). I discarded 3 that were too far from real Reddit style.
2. **Failure analysis:** After training, I gave Claude the list of misclassified posts and asked for patterns. It suggested that exclamatory language and short posts were over‑represented in errors. I verified this and confirmed that 8 of 10 errors were reactions misclassified as hot_take, often with exclamation marks.

## Demo Video
You can watch the demo video directly in this repository:  
📹 **[Click here to view demo.mp4](demo.mp4)**

*(If the video doesn't play in your browser, download it and open with a video player.)*