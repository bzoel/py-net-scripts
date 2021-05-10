# find_replace_mask.py

Find a list of CUCM translation patterns that have a calledPartyTransformationMask of <mask_to_find>. If a <mask_to_replace_with> is defined, offer to replace the calledPartyTransformationMask.

To find a list of translation patterns that contain a matching calledPartyTransformationMask
```
find_replace_mask.py <mask_to_find>
```

To find a list of translation patterns that contain a matching calledPartyTransformationMask, and replace them with a specific mask
```
find_replace_mask.py <mask_to_find> <mask_to_replace_with>
```
