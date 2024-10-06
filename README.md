# Multi-Dimensional Insights:  Benchmarking Real-World Personalization in Large Multimodal Models

![Dataset](https://img.shields.io/badge/Dataset-MDI--Benchmark-green)
![Multi-Modal](https://img.shields.io/badge/Task-Multi--Modal-red)
![Mathematical Reasoning](https://img.shields.io/badge/Task-Real_world_Reasoning-red) 

<p align="center">
    <img src="./assets/icon.png" width="35%"> <br>
</p>

## Outlines
- [💥 News 💥](README.md#-news-)
- [👀 About MDI-Benchmark]()
- [🏆 Leaderboard on MDI-Benchmark 🏆](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/README.md#-leaderboard-on-MDI-Benchmark-)
- [📝 Evaluation Piplines on MDI-Benchmark](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/README.md#-evaluation-piplines-on-MDI-Benchmark)
- [📊 MDI-Benchmark Dataset](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/README.md#-MDI-Benchmark-dataset)
- [📜 License](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/README.md#-license)
- [🤝 Contributors](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/README.md#-contributors)

## 💥 News 💥
  **[2023.10.8]** Our paper is now accessible at .

  **[2024.7.2]** Our dataset is now accessible at [Huggingface Datasets]().

  **[2024.10.8]** Our project homepage can be accessed at https://MDI-Benchmark.github.io/.

## 👀 About MDI-Benchmark
To align with the actual needs of humans for Large Multimodal Models, we propose a multi-modal benchmark for providing a thorough assessment of the capacities of LMMs in practical, real-world scenarios.

<p align="center">

```
<img src="./assets/fig1.png" alt="Overview of MDI-Benchmark" style="width: 85%;"> <br>
The overview of the <b>MDI-Benchmark</b> six real-world multimodal scenarios.
```

</p>

The MDI-Benchmark includes over 500 real-world images and 1.2k human-posed questions, spanning six real-world multimodal scenarios. Each scenario is divided into 3 sub-domains with 2 levels of complexity. Additionally, we incorporate age factors into the evaluation to guide LMMs in personalizing their responses for different demographic groups.

<p align="center">

```
<img src="./assets/fig2.png" alt="MDI-Benchmark question" style="width: 65%;"> <br>
The MDI-Benchmark includes real needs of different age groups in six major real-world scenarios.
```

</p>

With the MDI-Benchmark, we conduct a comprehensive evaluation of several mainstream LMMs. Specifically, GPT-4o achieved the best results across all indicators, but there is still significant room for improvement in addressing the needs of different age groups. Further analysis across dimensions such as Scenario, Complexity and Age provides valuable insights for developing reliable, personalized human assistants.

<p align="center">

```
<img src="./assets/leaderboard.png" alt="leaderboard" style="width: 95%;"> <br>
Performance of the model at different difficulty levels and the overall performance results of the model under the score metric.
```

</p>

We hope our research will advance the application of multimodal large models in real-world scenarios and pave the way for the development of multi-dimensional personalization.




## 🏆 Leaderboard on MDI-Benchmark 🏆
🚨🚨 The [Leaderboard](https://MDI-Benchmark.github.io/#leaderboard) is continuously being updated. We welcome the results of your model!
To submit your results to the leaderboard on the **testmini** subset, please send to [this email](mailto:qrq@bupt.edu.cn) with your result JSON file and score CSV file.

## 📝 Evaluation Piplines on MDI-Benchmark

### Response Generation 
The models generate responses based on the given questions and images. Examples for generating responses from some LMMs are provided in the [evaluation](./evaluation). Our prompt specifies the format of answer generation to facilitate subsequent extraction of the answer using string matching. Please refer to the following template to prepare your result JSON files for subsequent evaluation.
```json
{
    "ID": "3steps_165",
    "split": "testmini",
    "knowledge concept": "Area of Circles",
    "question": "As shown in the figure, there is a circular flower bed. Mary walked from the northernmost point of the flower bed along the edge to the easternmost point, taking a total of 80 steps. It is known that Mary's average step length is 0.628 cm, what is the area of the flower bed (  ) m²?(π = 3.14)",
    "option": "A. 200.96;B. 3215.36;C. 6280;D. 32; E. No correct answer",
    "answer": "B",
    "image_path": "3steps/image/165-3.png",
    "key": "3steps_3",
    "question number": 1575,
    "knowledge concept description": "Area of ...",
    "response": "<Thought process>: ... <Answer>: ..."
}
```
### Score Calculation
Due to the multiple-choice question format of our dataset and the specific answer generation prompt, we use string matching to directly extract answers, which eliminates the high cost of using additional models for further answer extraction.  The extracted answer is normalized to an option letter and calculate scores on our proposed four-dimensional metrics in [four_dimensional_metrics.py](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/evaluation/four_dimensional_metrics.py).
```sh
cd evaluation

python four_dimensional_metrics_refine.py \
--model_name GPT-4o \
--output_json ../output/GPT-4o.json  \
--main_results_csv_path ../result/four_dimensional_metrics.csv
```

Performences on One-Step / Two-Step / Three-Step problems and different problem domains are obtained from [accuracy.py](https://github.com/MDI-Benchmark/MDI-Benchmark/blob/main/evaluation/accuracy.py).

```sh
cd evaluation

python accuracy.py \
--model_name GPT-4o \
--output_json ../output/GPT-4o.json  \
--knowledge_structure_nodes_path /data/knowledge_structure_nodes.json \
```


## 📊 MDI-Benchmark Dataset

### Metric for Reasoning Evaluation
Based on the decomposed multi-step problems, we further reveal the inherent issues of LMMs in problem-solving process. We feed both the M one-step sub-problems and the original problem into LMMs, and classifying the responses into four categories
1. Insufficient Knowledge (IK): Part of one-step problems contain errors, and the multi-step problem is wrong. It is reasonable because model's insufficient grasp of single knowledge concept may lead to errors in multi-step problem.
2. Inadequate Generalization (IG): One-Step problems are all correct, but the multi-step problem is incorrect. This is also considered reasonable. While LMMs are capable of understanding individual knowledge concepts, they may struggle to generalize that knowledge to solve composite problems.
3. Complete Mastery (CM): One-Step problems are all correct, and multi-step problem is also answered correctly. This result demonstrates that the model's results are both reliable and accurate.
4. Rote Memorization (RM): One-Step problems contain errors, but the multi-step problem is answered correctly, which contradicts human logical thinking. If a model can solve composite multi-step problems but fails to answer the one-step problems needed in the process, it raises doubts about the model's reliability.

### Exmaples
<details>
<summary>🔍Examples of samples.</summary>
<p align="center">
    <img src="assets/example-2.png" width="90%"> <br>
</p>
</details>

### Knowledge cards
<details>
<summary>🔍Examples of Knowledge cards.</summary>
<p align="center">
    <img src="assets/example-card.png" width="90%"> <br>
</p>
</details>


## 📜 License

Our dataset are distributed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.


## :white_check_mark: Cite

If you find **MDI-Benchmark** useful for your your research and applications, please kindly cite using this BibTeX:

```bibtex
@misc{ 
}
```


## 🤝 Contributors
Here are the key contributors to this project:

Yifan Zhang, Shanglin Lei, Runqi Qiao, Zhuoma GongQue, Xiaoshuai Song, Guanting Dong, Qiuna Tan, Zhe Wei, Peiqing Yang, Ye Tian, Xiaofei Wang, Honggang Zhang