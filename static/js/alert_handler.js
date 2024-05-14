function handleAlertFadeOut(node) {
    setTimeout(function() {
        node.style.opacity = '0';
        setTimeout(function() {
            node.style.display = 'none';
        }, 500);
    }, 4000);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert').forEach(handleAlertFadeOut);
});