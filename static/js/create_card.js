const DELAY = 30;

const SELECTORS = {
    cardPreview: '#card-preview',
    slotImage: '.slot-image',
    slotPreview: '#slots-preview',
    dataSlotUuid: 'data-slot-id',
    slotsContainer: 'slots-container',
    slotTitleInput: '.slot-title-input',
};
const CLASSES = {
    dragging: 'dragging',
};

function getCardPreviewElement() {
    return document.querySelector(SELECTORS.cardPreview);
}

function getCardPreviewRect() {
    return getCardPreviewElement().getBoundingClientRect();
}

function updateImageSize(slider) {
    const slotUuid = slider.getAttribute(SELECTORS.dataSlotUuid);
    const slotImage = document.getElementById(`slot-img-${slotUuid}`);
    const gemImage = document.getElementById(`gem-img-${slotUuid}`);
    if (slotImage) {
        const newSize = slider.value;
        slotImage.style.width = `${newSize}px`;
        slotImage.style.height = 'auto';
        updateImageProperties(slotUuid, slotProperties, slotImage);

        if (gemImage) {
            const gemSize = newSize * 0.99;
            gemImage.style.width = `${gemSize}px`;
            gemImage.style.height = 'auto';
            updateImageProperties(slotUuid, gemProperties, gemImage);
        }
    }
}

function handleDragStart(e, clone) {
    e.target.classList.add(CLASSES.dragging);
    e.dataTransfer.setData('text', e.target.id);
    e.dataTransfer.effectAllowed = 'move';
    clone.current = e.target.cloneNode(true);
    clone.current.style.position = 'absolute';
    clone.current.style.pointerEvents = 'none';
    getCardPreviewElement().appendChild(clone.current);

    const rect = e.target.getBoundingClientRect();
    clone.offsetX = e.clientX - rect.left;
    clone.offsetY = e.clientY - rect.top;
}

function handleDrag(e, clone) {
    if (clone.current) {
        const cardPreviewRect = getCardPreviewRect();
        let newLeft = e.clientX - clone.offsetX - cardPreviewRect.left;
        let newTop = e.clientY - clone.offsetY - cardPreviewRect.top;

        if (newLeft + clone.current.offsetWidth / 2 >= 0 && newLeft + clone.current.offsetWidth / 2 <= cardPreviewRect.width &&
            newTop + clone.current.offsetHeight / 2 >= 0 && newTop + clone.current.offsetHeight / 2 <= cardPreviewRect.height) {
            clone.current.style.left = `${newLeft}px`;
            clone.current.style.top = `${newTop}px`;

            const slotUuid = e.target.getAttribute(SELECTORS.dataSlotUuid);
            updateImageProperties(slotUuid, slotProperties, clone.current);

            const gemImage = document.getElementById(`gem-img-${slotUuid}`);
            if (gemImage) {
                const gemSize = gemImage.offsetWidth;
                gemImage.style.left = `${newLeft + (clone.current.offsetWidth - gemSize) / 2}px`;
                gemImage.style.top = `${newTop + (clone.current.offsetHeight - gemSize) / 2}px`;
                updateImageProperties(slotUuid, gemProperties, gemImage);
            }
        }
    }
}

function handleDragEnd(e, clone) {
    if (clone.current) {
        const cardPreviewRect = getCardPreviewRect();
        let newLeft = parseFloat(clone.current.style.left);
        let newTop = parseFloat(clone.current.style.top);

        newLeft = Math.max(-clone.current.offsetWidth / 2, Math.min(newLeft, cardPreviewRect.width - clone.current.offsetWidth / 2));
        newTop = Math.max(-clone.current.offsetHeight / 2, Math.min(newTop, cardPreviewRect.height - clone.current.offsetHeight / 2));

        e.target.style.left = `${newLeft}px`;
        e.target.style.top = `${newTop}px`;

        const slotUuid = e.target.getAttribute(SELECTORS.dataSlotUuid);

        const xPositionInput = document.getElementById(`id_slots-${slotUuid}-x_position`);
        const yPositionInput = document.getElementById(`id_slots-${slotUuid}-y_position`);

        if (xPositionInput && yPositionInput) {
            xPositionInput.value = (newLeft + clone.current.offsetWidth / 2) / cardPreviewRect.width;
            yPositionInput.value = (newTop + clone.current.offsetHeight / 2) / cardPreviewRect.height;
        }

        updateImageProperties(slotUuid, slotProperties, e.target);

        const gemImage = document.getElementById(`gem-img-${slotUuid}`);
        if (gemImage) {
            const gemSize = gemImage.offsetWidth;
            gemImage.style.left = `${newLeft + (clone.current.offsetWidth - gemSize) / 2}px`;
            gemImage.style.top = `${newTop + (clone.current.offsetHeight - gemSize) / 2}px`;
            updateImageProperties(slotUuid, gemProperties, gemImage);
        }

        getCardPreviewElement().removeChild(clone.current);
        clone.current = null;
    }
    e.target.classList.remove(CLASSES.dragging);
}

function makeImageDraggable(img) {
    const clone = {current: null};

    img.setAttribute('draggable', 'true');
    img.addEventListener('dragstart', (e) => handleDragStart(e, clone));
    img.addEventListener('drag', (e) => handleDrag(e, clone));
    img.addEventListener('dragend', (e) => handleDragEnd(e, clone));
}

function updateSlotTitle(input) {
    input.addEventListener('input', function () {
        const slotElement = this.closest('.slot');
        const slotTitleElement = slotElement ? slotElement.querySelector('.slot-title') : null;
        const offcanvasTitleElement = slotElement ? slotElement.querySelector('.offcanvas-title') : null;
        if (slotTitleElement) {
            slotTitleElement.textContent = this.value;
        }
        if (offcanvasTitleElement) {
            offcanvasTitleElement.textContent = this.value;
        }
    });
}

function applyStoredProperties(slotUuid, propertiesDict, imageElement) {
    const properties = propertiesDict[slotUuid];
    if (properties) {
        setTimeout(() => {
            imageElement.style.width = properties.width;
            imageElement.style.height = properties.height;
            imageElement.style.left = properties.left;
            imageElement.style.top = properties.top;
        }, DELAY);
    }
}


function updateImageProperties(slotUuid, propertiesDict, imageElement) {
    propertiesDict[slotUuid] = {
        width: imageElement.style.width,
        height: imageElement.style.height,
        left: imageElement.style.left,
        top: imageElement.style.top,
    };
}


function centerGem(slotImage, gemImage) {
    if (!slotImage) {
        return;
    }
    const slotLeft = parseFloat(slotImage.style.left);
    const slotTop = parseFloat(slotImage.style.top);
    const gemSize = gemImage.offsetWidth;

    const gemLeft = slotLeft + (slotImage.offsetWidth - gemSize) / 2;
    const gemTop = slotTop + (slotImage.offsetHeight - gemSize) / 2;

    setTimeout(() => {
        gemImage.style.width = `${gemSize}px`;
        gemImage.style.height = 'auto';
        gemImage.style.left = `${gemLeft}px`;
        gemImage.style.top = `${gemTop}px`;
    }, DELAY);
}

function initializeEventListeners() {
    const slotPreview = document.querySelector(SELECTORS.slotPreview);
    const slotsContainer = document.getElementById(SELECTORS.slotsContainer);

    slotsContainer.addEventListener('input', function (event) {
        if (event.target.type === 'range' && event.target.hasAttribute(SELECTORS.dataSlotUuid)) {
            updateImageSize(event.target);
        }
    });

    slotPreview.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    slotPreview.addEventListener('drop', (e) => {
        e.preventDefault();
        const imgId = e.dataTransfer.getData('text');
        const img = document.getElementById(imgId);
        if (img) {
            const parentPosition = slotPreview.getBoundingClientRect();
            img.style.position = 'absolute';
            img.style.left = `${e.clientX - parentPosition.left - img.offsetWidth / 2}px`;
            img.style.top = `${e.clientY - parentPosition.top - img.offsetHeight / 2}px`;
        }
    });

    document.querySelectorAll(SELECTORS.slotImage).forEach(makeImageDraggable);

    document.querySelectorAll(SELECTORS.slotTitleInput).forEach(updateSlotTitle);

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes) {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        const slotTitleInput = node.querySelector(SELECTORS.slotTitleInput);
                        if (slotTitleInput) {
                            updateSlotTitle(slotTitleInput);
                        }
                        if (node.matches(SELECTORS.slotImage)) {
                            makeImageDraggable(node);
                        }
                        if (node.classList.contains('image-slot-gem-container')) {
                            const slotUuid = node.id.match(/slot-container-(\d+)/)[1];

                            const slotImageContainer = node.querySelector('.image-slot-container');
                            const gemImageContainer = node.querySelector('.image-gem-container');

                            const slotImageObserver = new MutationObserver((slotMutations) => {
                                slotMutations.forEach((slotMutation) => {
                                    slotMutation.addedNodes.forEach((slotNode) => {
                                        if (slotNode.nodeType === 1 && slotNode.classList.contains('slot-image')) {
                                            applyStoredProperties(slotUuid, slotProperties, slotNode);
                                        }
                                    });
                                });
                            });

                            const gemImageObserver = new MutationObserver((gemMutations) => {
                                gemMutations.forEach((gemMutation) => {
                                    gemMutation.addedNodes.forEach((gemNode) => {
                                        if (gemNode.nodeType === 1 && gemNode.classList.contains('gem-image')) {
                                            applyStoredProperties(slotUuid, gemProperties, gemNode);
                                            centerGem(slotImageContainer.querySelector('.slot-image'), gemNode);
                                        }
                                    });
                                });
                            });

                            slotImageObserver.observe(slotImageContainer, {childList: true});
                            gemImageObserver.observe(gemImageContainer, {childList: true});
                        }
                    }
                });
            }
        });
    });

    observer.observe(document.body, {childList: true, subtree: true});
}

const slotProperties = {};
const gemProperties = {};

document.addEventListener('DOMContentLoaded', initializeEventListeners);

function removeSlot(button) {
    const slotId = button.getAttribute('data-slot-id');
    const slotElement = document.querySelector(slotId);
    if (slotElement) {
        slotElement.classList.add("deleted");
        const deleteInput = document.querySelector(
            `#id_slots-${slotId.split('#slot')[1]}-DELETE`);
        if (deleteInput) {
            deleteInput.value = 'on';
        }
        const imageSelect = document.querySelector(`#id_slots-${slotId.split('#slot')[1]}-image`);
        if (imageSelect) {
            imageSelect.disabled = true;
        }
    }
}