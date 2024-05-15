const PRESET_SELECTORS = {
    preset: '#id_preset',
    outline: '#id_outline',
    slotsContainer: '#slots-container',
    cardPreview: '#card-preview',
};

function dispatchChangeEvent(element) {
    const event = new Event('change');
    element.dispatchEvent(event);
}

function createSlot(slot, index) {
    htmx.ajax('GET', `htmx/slot/create?total_forms=${index}`, {
        target: PRESET_SELECTORS.slotsContainer,
        swap: 'beforeend',
        values: {'total_forms': index},
    }).then(() => {
        document.getElementById(`id_slots-${index}-title`).value = slot.title;
        const imageSelect = document.getElementById(`id_slots-${index}-image`);
        if (imageSelect) {
            imageSelect.value = slot.image_id;
            htmx.process(imageSelect);
            dispatchChangeEvent(imageSelect);
        }
        document.getElementById(`id_slots-${index}-size`).value = slot.size;
        document.getElementById(`id_slots-${index}-x_position`).value = slot.x_position;
        document.getElementById(`id_slots-${index}-y_position`).value = slot.y_position;

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes) {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1 && node.id === `slot-img-${index}`) {
                            const previewContainer = document.querySelector(PRESET_SELECTORS.cardPreview);
                            const previewContainerRect = previewContainer.getBoundingClientRect();
                            let leftInPixels = slot.x_position * previewContainerRect.width;
                            let topInPixels = slot.y_position * previewContainerRect.height;

                            leftInPixels -= slot.size / 2;
                            topInPixels -= slot.size / 2;
                            node.style.left = `${leftInPixels}px`;
                            node.style.top = `${topInPixels}px`;
                            node.style.width = `${slot.size}px`;

                            observer.disconnect();
                        }
                    });
                }
            });
        });
        observer.observe(document.body, {childList: true, subtree: true});
    });
}

function handlePresetChange() {
    const presetId = this.value;
    if (presetId) {
        fetch(`presets/${presetId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const outlineSelect = document.querySelector(PRESET_SELECTORS.outline);
                if (outlineSelect) {
                    outlineSelect.value = data.outline_id;
                    htmx.process(outlineSelect);
                    dispatchChangeEvent(outlineSelect);
                }
                data.slots.forEach((slot, index) => {
                    createSlot(slot, index);
                });
            })
            .catch(e => {
                console.log('There was a problem with the fetch operation: ' + e.message);
            });
    }
}

document.querySelector(PRESET_SELECTORS.preset).addEventListener('change', handlePresetChange);