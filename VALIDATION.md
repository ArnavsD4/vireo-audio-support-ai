# Model validation

## What was tested

A TF-IDF + Logistic Regression text classifier was trained on:

`customer_message + agent_notes`

The model was evaluated using a stratified 20% hold-out set.

The source `category` field is the existing intake/agent tag, not independently verified ground truth. Therefore, the hold-out result measures **agreement with the current tagging system**, not absolute real-world classification accuracy.

### Hold-out results

- Analysis tickets: **11,641**
- Training rows: **9,312**
- Hold-out rows: **2,329**
- Agreement with existing category tags: **83.7%**

## Classification report

```text
                     precision    recall  f1-score   support

Account & Login          0.847     0.923     0.883        78
App & Firmware           0.825     0.807     0.816       140
Audio Quality            0.783     0.949     0.858       118
Billing & Payments      0.887     0.905     0.896       485
Charging & Battery      0.817     0.896     0.855       164
Connectivity             0.855     0.935     0.893       201
Delivery & Shipping      0.794     0.890     0.839       381
Other                    0.816     0.449     0.579       325
Product Enquiry          0.867     0.959     0.911       122
Returns & Refunds        0.852     0.929     0.888       210
Warranty & Repair        0.818     0.771     0.794       105

accuracy                           0.837      2329
macro avg                0.833     0.856     0.838      2329
weighted avg             0.836     0.837     0.828      2329