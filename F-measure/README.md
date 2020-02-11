# F-measure
<font size = 4> 
The performance of the contest is measured by the harmonic mean of Precision and Recall.<br><br>
Precision (P) = True Positive / (True Positive + False Positive)<br>
Recall (R) = True Positive / (True Positive + False Negative)<br>
F-measure(F1) = 2*P*R / (P + R)
</font>

# How to calculate?
<font size = 4>
Ground Truth:   <b>labeled_dataset.csv</b><br>
Our submission: <b>submission.csv</b>

A matched pair can be considered as two nodes of an edge in graph G, then the aboving files can be expressed by the following Graphs.

Ground Truth:<br>
<img src="https://pic.downk.cc/item/5e42764b2fb38b8c3ca0b7f3.png" width=35% height=50%>

Our submission:<br>
<img src="https://pic.downk.cc/item/5e4277502fb38b8c3ca0dc1b.png" width=35% height=50%>

Calculation:<br>
<img src="https://pic.downk.cc/item/5e4277b22fb38b8c3ca0e8e1.png"  width=70% height=50%>
</font>