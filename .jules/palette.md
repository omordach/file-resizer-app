## 2024-03-24 - Dropzone Accessibility and Preview Constraints
**Learning:** Dropzones without visual focus indicators break keyboard navigation completely as users cannot tell when they are focused. Image previews lacking max-height bounds can break the layout entirely for tall source images.
**Action:** Always add `focus-visible:ring` to interactive drop zones, and constraint user-uploaded images with `max-h` and `object-contain`.
