document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.querySelector('.sidebar');
    sidebar.addEventListener('mouseenter', function() {
        sidebar.classList.add('expanded');
    });

    sidebar.addEventListener('mouseleave', function() {
        sidebar.classList.remove('expanded');
    });
});

$(document).ready(function() {
    $('.dropdown-toggle').dropdown();
});