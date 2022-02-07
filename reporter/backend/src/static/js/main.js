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

    function adjustDiffNode(node) {
        const bootstrapStyle = getBootstrapStyle()
        if (['None', '0.00', '$0.00'].includes(node.textContent)) {
            node.textContent = ''
        } else if (node.textContent.startsWith('-')) {
            node.style.color = bootstrapStyle.color.danger
        } else {
            node.textContent = '+' + node.textContent
            node.style.color = bootstrapStyle.color.success
        }
    }

    function setPlainDifference() {
        const differences = document.querySelectorAll('.plain-difference')
        differences.forEach((difference) => {
                adjustDiffNode(difference)
            }
        )
    }

    function setPercentDifference() {
        const differences = document.querySelectorAll('.percent-difference')
        differences.forEach((difference) => {
                adjustDiffNode(difference)
                if (difference.textContent) {
                    difference.textContent += '%'
                }
            }
        )
    }

    setPlainDifference()
    setPercentDifference()
})