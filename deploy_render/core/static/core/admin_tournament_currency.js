// Dynamically update the prize amount display in the TeamTournamentResult inline when currency changes
(function() {
    function updatePrizeLabels() {
        // Find all inlines for TeamTournamentResult
        document.querySelectorAll('.dynamic-teamtournamentresult_set').forEach(function(inline) {
            var currencySelect = inline.querySelector('select[id$="-currency"]');
            var prizeInput = inline.querySelector('input[id$="-prize_amount"]');
            var label = inline.querySelector('.prize-amount-label');
            if (!label) {
                // Create a label if it doesn't exist
                label = document.createElement('span');
                label.className = 'prize-amount-label';
                label.style.marginLeft = '8px';
                prizeInput && prizeInput.parentNode.appendChild(label);
            }
            if (currencySelect && prizeInput && label) {
                var currency = currencySelect.options[currencySelect.selectedIndex].text;
                var value = prizeInput.value;
                label.textContent = value ? `${currency} ${value}` : '';
            }
            if (currencySelect) {
                currencySelect.addEventListener('change', function() {
                    var currency = currencySelect.options[currencySelect.selectedIndex].text;
                    var value = prizeInput.value;
                    label.textContent = value ? `${currency} ${value}` : '';
                });
            }
            if (prizeInput) {
                prizeInput.addEventListener('input', function() {
                    var currency = currencySelect.options[currencySelect.selectedIndex].text;
                    var value = prizeInput.value;
                    label.textContent = value ? `${currency} ${value}` : '';
                });
            }
        });
    }
    // Run on page load and when inlines are added
    document.addEventListener('DOMContentLoaded', updatePrizeLabels);
    document.body.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('add-row')) {
            setTimeout(updatePrizeLabels, 100);
        }
    });
})(); 