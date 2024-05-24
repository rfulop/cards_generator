const PRESET_SELECTORS = {
    preset: '#id_preset',
    outline: '#id_outline',
    slotsContainer: '#slots-container',
    initialSlotsData: 'initial-slots-data',
    slotsPreview: '#slots-preview',
};

function init() {
    if (isUpdate) {
        document.addEventListener("DOMContentLoaded", () => {
            initializeOutlinePreview();
            initializeSlots();
        });
    }

    document.querySelector(PRESET_SELECTORS.preset).addEventListener('change', handlePresetChange);
}

function dispatchChangeEvent(element) {
    const event = new Event('change');
    element.dispatchEvent(event);
}

function updateOutlinePreview(outlineId) {
    const outlineSelect = document.querySelector(PRESET_SELECTORS.outline);
    if (outlineSelect) {
        outlineSelect.value = outlineId;
        htmx.process(outlineSelect);
        dispatchChangeEvent(outlineSelect);
    }
}

function updateSlotFields(index, slot) {
    document.getElementById(`id_slots-${index}-title`).value = slot.title;
    const imageSelect = document.getElementById(`id_slots-${index}-image`);
    const gemSelect = document.getElementById(`id_slots-${index}-gem`);
    const sizeInput = document.getElementById(`id_slots-${index}-size`);
    const xPosInput = document.getElementById(`id_slots-${index}-x_position`);
    const yPosInput = document.getElementById(`id_slots-${index}-y_position`);
    const textInput = document.getElementById(`id_slots-${index}-text`);

    if (imageSelect) {
        imageSelect.value = slot.image_id;
        htmx.process(imageSelect);
        dispatchChangeEvent(imageSelect);
    }

    if (gemSelect) {
        gemSelect.value = slot.gem_id;
        htmx.process(gemSelect);
        dispatchChangeEvent(gemSelect);
    }

    if (textInput) {
        htmx.process(textInput);
        textInput.value = slot.text;
        dispatchChangeEvent(textInput);
    }

    sizeInput.value = slot.size;
    xPosInput.value = slot.x_position;
    yPosInput.value = slot.y_position;
}

function positionSlotContainer(index, slot) {
    const slotContainer = document.querySelector(`#slot-container-${index}`);
    slotContainer.style.position = 'absolute';
    slotContainer.style.width = `${slot.size}px`;
    slotContainer.style.height = `${slot.size}px`;
    const left = slot.x_position - slot.size / 2;
    const top = slot.y_position - slot.size / 2;
    slotContainer.style.left = `${left}px`;
    slotContainer.style.top = `${top}px`;
}

async function createSlot(slot, index) {
    try {
        await htmx.ajax('GET', `${createSlotUrl}?total_forms=${index}`, {
            target: PRESET_SELECTORS.slotsContainer,
            swap: 'beforeend',
            values: {'total_forms': index},
        });

        const titleInput = document.querySelector(`#id_slots-${index}-title`);
        if (titleInput) {
            updateSlotFields(index, slot);
            positionSlotContainer(index, slot);
        } else {
            console.error(`titleInput not found after request for slot ${index}`);
        }
    } catch (error) {
        console.error(`Request failed for slot ${index}:`, error);
        throw error;
    }
}

function resetSlots() {
    const slotsContainer = document.querySelector(PRESET_SELECTORS.slotsContainer);
    slotsContainer.innerHTML = '';

    const slotsPreview = document.querySelector(PRESET_SELECTORS.slotsPreview);
    slotsPreview.innerHTML = '';
}

function initializeOutlinePreview() {
    const initialOutlineId = document.querySelector(PRESET_SELECTORS.outline).value;
    if (initialOutlineId) {
        updateOutlinePreview(initialOutlineId);
    }
}

async function initializeSlots() {
    const initialSlotsDataElement = document.getElementById(PRESET_SELECTORS.initialSlotsData);
    if (initialSlotsDataElement) {
        const initialSlots = JSON.parse(initialSlotsDataElement.textContent);
        await createSlots(initialSlots);
    }
}

async function createSlots(slots) {
    for (let index = 0; index < slots.length; index++) {
        await createSlot(slots[index], index);
    }
}

async function handlePresetChange(event) {
    const presetId = event.target.value;
    if (presetId) {
        const url = `${presetDetailsBaseUrl}${presetId}/details`;
        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.error(`HTTP error! status: ${response.status}`);
                return;
            }
            const data = await response.json();
            updateOutlinePreview(data.outline_id);
            resetSlots();
            await createSlots(data.slots);
        } catch (e) {
            console.error('There was a problem with the fetch operation: ' + e.message);
        }
    }
}

init();
