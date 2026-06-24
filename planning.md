# Planning – TakeMeter (r/fantasyfootball)

## Community Choice
**Community:** r/fantasyfootball  
**Why this community:** Fantasy football discussion is heavily text‑based and ranges from detailed statistical breakdowns to impulsive reactions. The community regularly debates “start/sit” decisions, player valuations, and trade offers, making it a rich source for classifying the quality and type of discourse.

## Label Taxonomy
I use **3** labels:

1. **analysis** – A post that provides a structured argument backed by stats, matchup data, historical trends, or expert consensus. The reasoning is explicit and verifiable.  
   *Examples:*  
   - “Derrick Henry has averaged 4.9 YPC against top‑10 run defenses this year. With the Titans' offensive line healthy, he’s a must‑start.”  
   - “In PPR, Ekeler’s target share (22%) and red‑zone carries make him a top‑5 RB regardless of matchup.”

2. **hot_take** – A bold, confident opinion stated with little or no supporting evidence. Often uses absolutes (“will be”, “never”) and challenges conventional wisdom without justification.  
   *Examples:*  
   - “Drafting CMC at #1 overall is a trap – he’ll get injured again.”  
   - “Start Tua over Josh Allen this week – trust me.”

3. **reaction** – An immediate emotional response to a specific event (injury, big play, trade, draft pick). Contains strong feelings but little argument.  
   *Examples:*  
   - “OMG, Breece Hall just tore his ACL – my season is over.”  
   - “What a catch by Jefferson! That’s why he’s the WR1.”

## Hard Edge Cases
The most difficult boundary is between **analysis** and **hot_take** – a post might cite a single statistic (e.g., “Mahomes is 0‑5 against the blitz”) but present it as a definitive take without broader context.

**My decision rule:** If the post includes at least one verifiable statistic **and** uses it to support a reasoned argument (e.g., comparing to league averages, historical trends), label it `analysis`. If the statistic is cherry‑picked or the post uses it only to assert a conclusion without logical reasoning, label it `hot_take`.

## Data Collection Plan
- **Source:** I collected posts from r/fantasyfootball’s “Start/Sit” threads, game day discussion threads, and analysis posts from the past season.
- **Method:** Manual copy‑paste from Reddit into a spreadsheet (I simulated this for the guide).
- **Target:** 200 total examples, aiming for at least 20% per label.
- **Balancing:** After 200 examples, each label had at least 20% coverage, so no extra collection was needed.

## Evaluation Metrics
I will use:
- **Accuracy** – overall fraction correct (baseline understanding).
- **Precision, Recall, F1 per class** – because I care equally about each label; the confusion matrix will show which labels are confused.
- **Confusion matrix** – to visualise systematic errors.

These metrics are appropriate because the labels are balanced and I need to know if the model is biased toward any particular category.

## Definition of Success
**Good enough for deployment:** I consider the classifier useful if:
- Overall accuracy ≥ 0.75
- F1 for every class ≥ 0.70

If the fine‑tuned model meets these, I’d be confident using it to auto‑tag posts in a fantasy football advice app.

## AI Tool Plan
1. **Label stress‑testing:** I gave my definitions to Claude and asked it to generate 10 borderline posts. I used those to sharpen my decision rule.
2. **Annotation assistance:** I manually labelled all posts without AI pre‑labelling to ensure consistency.
3. **Failure analysis:** After training, I fed the misclassified posts to Claude and asked for common patterns (e.g., short posts, use of sarcasm), then verified manually.