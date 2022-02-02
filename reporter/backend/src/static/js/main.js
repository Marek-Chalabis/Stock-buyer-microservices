document.addEventListener('DOMContentLoaded', () => {
    function getBootstrapStyle() {
        const bootstrapStyle = getComputedStyle(document.body);
        return {
            color: {
                success: bootstrapStyle.getPropertyValue('--success'),
                danger: bootstrapStyle.getPropertyValue('--danger')
            }
        }
    }

    function setColorForPriceDifference() {
        const priceDifferences = document.querySelectorAll('.price-difference')
        const bootstrapStyle = getBootstrapStyle();
        priceDifferences.forEach((priceDifferance) => {
            const difference = priceDifferance.textContent.split('%')[0]
            if (difference) {
                priceDifferance.style.color = difference > 0
                    ? bootstrapStyle.color.success
                    : bootstrapStyle.color.danger
            }
        })
    }

    setColorForPriceDifference()
})