class CardForm {
    constructor() {
        this.PRESET_SELECTORS = {
            preset: '#id_preset',
            outline: '#id_outline',
            slotsContainer: '#slots-container',
            cardPreview: '#card-preview',
            outlinePreview: '#outline-preview',
            slotsPreview: '#slots-preview'
        };

        this.createSlotUrl = createSlotUrl;
        this.presetDetailsBaseUrl = presetDetailsBaseUrl;

        this.isUpdate = isUpdate;

        this.initEventListeners();
    }

    static init() {
        new CardForm();
    }

    initEventListeners() {
        if (this.isUpdate) {
            document.addEventListener("DOMContentLoaded", () => {
                this.initializeOutlinePreview();
                this.initializeSlots();
            });
        }

        document.querySelector(this.PRESET_SELECTORS.preset).addEventListener('change', (event) => {
            this.handlePresetChange(event);
        });
    }

    dispatchChangeEvent(element) {
        const event = new Event('change');
        element.dispatchEvent(event);
    }

    updateOutlinePreview(outlineId) {
        const outlineSelect = document.querySelector(this.PRESET_SELECTORS.outline);
        if (outlineSelect) {
            outlineSelect.value = outlineId;
            htmx.process(outlineSelect);
            this.dispatchChangeEvent(outlineSelect);
        }
    }

    updateSlotPreview(slot, index) {
        const observer = new MutationObserver((mutations, obs) => {
            const slotImage = document.getElementById(`slot-img-${index}`);
            if (slotImage) {
                const previewContainer = document.querySelector(this.PRESET_SELECTORS.cardPreview);
                const previewContainerRect = previewContainer.getBoundingClientRect();
                let leftInPixels = slot.x_position * previewContainerRect.width;
                let topInPixels = slot.y_position * previewContainerRect.height;

                leftInPixels -= slot.size / 2;
                topInPixels -= slot.size / 2;
                slotImage.style.left = `${leftInPixels}px`;
                slotImage.style.top = `${topInPixels}px`;
                slotImage.style.width = `${slot.size}px`;

                obs.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    async createSlots(slots) {
        for (let index = 0; index < slots.length; index++) {
            const slot = slots[index];
            await this.createSlot(slot, index);
        }
    }

    createSlot(slot, index) {
        return new Promise((resolve, reject) => {
            htmx.ajax('GET', `${this.createSlotUrl}?total_forms=${index}`, {
                target: this.PRESET_SELECTORS.slotsContainer,
                swap: 'beforeend',
                values: {'total_forms': index},
            }).then(() => {
                const titleInput = document.querySelector(`#id_slots-${index}-title`);
                if (titleInput) {
                    titleInput.value = slot.title;
                    const imageSelect = document.getElementById(`id_slots-${index}-image`);
                    if (imageSelect) {
                        imageSelect.value = slot.image_id;
                        htmx.process(imageSelect);
                        this.dispatchChangeEvent(imageSelect);
                    }
                    document.getElementById(`id_slots-${index}-size`).value = slot.size;
                    document.getElementById(`id_slots-${index}-x_position`).value = slot.x_position;
                    document.getElementById(`id_slots-${index}-y_position`).value = slot.y_position;
                    this.updateSlotPreview(slot, index);
                    resolve();
                } else {
                    console.error(`titleInput not found after request for slot ${index}`);
                    reject(new Error(`titleInput not found for slot ${index}`));
                }
            }).catch((error) => {
                console.error(`Request failed for slot ${index}:`, error);
                reject(error);
            });
        });
    }

    resetSlots() {
        const slotsContainer = document.querySelector(this.PRESET_SELECTORS.slotsContainer);
        while (slotsContainer.firstChild) {
            slotsContainer.removeChild(slotsContainer.firstChild);
        }

        const slotsPreview = document.querySelector(this.PRESET_SELECTORS.slotsPreview);
        while (slotsPreview.firstChild) {
            slotsPreview.removeChild(slotsPreview.firstChild);
        }
    }

    initializeOutlinePreview() {
        const initialOutlineId = document.querySelector(this.PRESET_SELECTORS.outline).value;
        if (initialOutlineId) {
            this.updateOutlinePreview(initialOutlineId);
        }
    }

    async initializeSlots() {
        const initialSlotsDataElement = document.getElementById('initial-slots-data');
        if (initialSlotsDataElement) {
            const initialSlots = JSON.parse(initialSlotsDataElement.textContent);
            await this.createSlots(initialSlots);
        }
    }

    handlePresetChange(event) {
        const presetId = event.target.value;
        if (presetId) {
            const url = `${this.presetDetailsBaseUrl}${presetId}/details`;
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    this.updateOutlinePreview(data.outline_id);
                    this.resetSlots();
                    data.slots.forEach((slot, index) => {
                        this.createSlot(slot, index);
                    });
                })
                .catch(e => {
                    console.log('There was a problem with the fetch operation: ' + e.message);
                });
        }
    }
}

CardForm.init();