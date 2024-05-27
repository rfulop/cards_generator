const SELECTORS = {
    dataSlotUuid: 'data-slot-id',
    slotsPreview: '#slots-preview',
    slotContainerPrefix: 'slot-container-',
    slotContainerClass: 'image-slot-gem-container',
    slotTextContainerClass: 'slot-text-container',
    slotTextClass: 'slot-text',
    inputTypeRange: 'range',
};

document.addEventListener('DOMContentLoaded', init);

function init() {
    document.body.addEventListener('input', handleSliderInput);

    document.addEventListener('dragover', handleDragOver);
    document.addEventListener('drop', handleDrop);

    const observer = new MutationObserver(handleMutations);
    observer.observe(document.body, {childList: true, subtree: true});
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();

    const data = JSON.parse(event.dataTransfer.getData('text/plain'));
    const container = document.getElementById(data.slotId);
    const parentRect = document.querySelector(SELECTORS.slotsPreview).getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();

    let left = event.clientX - data.offsetX;
    let top = event.clientY - data.offsetY;

    left = Math.max(parentRect.left, Math.min(left, parentRect.right - containerRect.width));
    top = Math.max(parentRect.top, Math.min(top, parentRect.bottom - containerRect.height));

    container.style.left = `${left - parentRect.left}px`;
    container.style.top = `${top - parentRect.top}px`;

    const slotUuid = container.getAttribute(SELECTORS.dataSlotUuid);
    const xPositionInput = document.getElementById(`id_slots-${slotUuid}-x_position`);
    const yPositionInput = document.getElementById(`id_slots-${slotUuid}-y_position`);

    if (xPositionInput && yPositionInput) {
        xPositionInput.value = left - parentRect.left + containerRect.width / 2;
        yPositionInput.value = top - parentRect.top + containerRect.height / 2;
    }
}

function handleSliderInput(event) {
    if (event.target.type === SELECTORS.inputTypeRange && event.target.hasAttribute(SELECTORS.dataSlotUuid)) {
        const slotId = event.target.getAttribute(SELECTORS.dataSlotUuid);
        const slotContainer = document.getElementById(`${SELECTORS.slotContainerPrefix}${slotId}`);
        const newSize = event.target.value;
        slotContainer.style.width = `${newSize}px`;
        slotContainer.style.height = `${newSize}px`;

        const slotText = slotContainer.querySelector(`.${SELECTORS.slotTextClass}`);
        if (slotText) {
            slotText.style.fontSize = `${newSize / 2}px`;
        }
    }
}

function updateSlotText(slotContainer) {
    const slotId = slotContainer.getAttribute(SELECTORS.dataSlotUuid);
    const fontSelect = document.getElementById(`id_slots-${slotId}-font`);
    if (fontSelect) {
        fontSelect.addEventListener('change', () => {
            const slotTextContainer = slotContainer.querySelector(`.${SELECTORS.slotTextContainerClass}`);
            if (slotTextContainer) {
                slotTextContainer.style.fontFamily = fontSelect.value;
            }
        });
    }
    const textColorInput = document.getElementById(`id_slots-${slotId}-text_color`);

    if (textColorInput) {
        const updateSlotColorText = function (event) {
            const slotTextContainer = slotContainer.querySelector(`.${SELECTORS.slotTextContainerClass}`);
            if (slotTextContainer) {
                slotTextContainer.style.color = textColorInput.value;
            }
        };
        textColorInput.addEventListener('change', updateSlotColorText);
        textColorInput.addEventListener('input', updateSlotColorText);
    }
}

function handleMutations(mutations) {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1 && node.classList.contains(SELECTORS.slotContainerClass)) {
                    makeContainerDraggable(node);
                    updateSlotText(node);
                }
            });
        }
    });
}

function makeContainerDraggable(container) {
    container.addEventListener('dragstart', (event) => {
        const rect = container.getBoundingClientRect();
        event.dataTransfer.setData('text/plain', JSON.stringify({
            slotId: container.id,
            offsetX: event.clientX - rect.left,
            offsetY: event.clientY - rect.top
        }));
    });
}