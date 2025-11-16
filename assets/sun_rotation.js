/**
 * Sun Icon Rotation on Scroll
 * Rotates the sun icon (light theme icon) while user scrolls
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sun rotation handler loaded');

    let scrollTimeout;
    let lastScrollY = window.scrollY;

    // Function to get sun icon (refreshed each time)
    function getSunIcon() {
        return document.getElementById('light-theme-icon');
    }

    // Function to add rotating class based on direction
    function startRotation(direction) {
        const sunIcon = getSunIcon();
        if (sunIcon) {
            // Remove both classes first
            sunIcon.classList.remove('rotating-up', 'rotating-down');

            // Add the appropriate class
            if (direction === 'down') {
                sunIcon.classList.add('rotating-down');
                console.log('Started sun rotation - clockwise (scrolling down)');
            } else {
                sunIcon.classList.add('rotating-up');
                console.log('Started sun rotation - counter-clockwise (scrolling up)');
            }
        } else {
            console.log('Sun icon not found');
        }
    }

    // Function to remove rotating classes
    function stopRotation() {
        const sunIcon = getSunIcon();
        if (sunIcon) {
            sunIcon.classList.remove('rotating-up', 'rotating-down');
            console.log('Stopped sun rotation');
        }
    }

    // Handle scroll event
    function handleScroll(event) {
        // Get scroll position from event target or window
        const scrollElement = event && event.target !== document ? event.target : window;
        const currentScrollY = scrollElement === window ? window.scrollY : scrollElement.scrollTop;

        // Determine scroll direction
        const scrollDirection = currentScrollY > lastScrollY ? 'down' : 'up';

        // Update last scroll position
        lastScrollY = currentScrollY;

        // Start rotation with direction
        startRotation(scrollDirection);

        // Clear existing timeout
        clearTimeout(scrollTimeout);

        // Stop rotation after 200ms of no scrolling for smoother deceleration
        scrollTimeout = setTimeout(function() {
            stopRotation();
        }, 200);
    }

    // Add scroll listener to window with debug
    window.addEventListener('scroll', handleScroll, { passive: true });
    console.log('Window scroll listener attached');

    // Function to attach scroll listeners to dash-dock containers
    function attachDockScrollListeners() {
        // Find all dash-dock tab content areas that can scroll
        const scrollableContainers = document.querySelectorAll('.flexlayout__tab, .flexlayout__tabset_content, [class*="dock"]');

        scrollableContainers.forEach(container => {
            if (!container.dataset.sunRotationAttached) {
                // Check if element is scrollable
                if (container.scrollHeight > container.clientHeight ||
                    getComputedStyle(container).overflowY === 'auto' ||
                    getComputedStyle(container).overflowY === 'scroll') {

                    container.addEventListener('scroll', handleScroll, { passive: true });
                    container.dataset.sunRotationAttached = 'true';
                    console.log('Attached scroll listener to dock container:', container.className);
                }
            }
        });
    }

    // Initial attachment
    setTimeout(attachDockScrollListeners, 500);
    setTimeout(attachDockScrollListeners, 1500);

    // Re-attach when DOM changes (for dynamically loaded content)
    const dockObserver = new MutationObserver(function(mutations) {
        clearTimeout(window.dockScrollTimeout);
        window.dockScrollTimeout = setTimeout(attachDockScrollListeners, 200);
    });

    dockObserver.observe(document.body, {
        childList: true,
        subtree: true
    });

    console.log('Dock scroll observer active');

    // Setup with MutationObserver for Dash page updates
    function setupSunRotation() {
        const newSunIcon = document.getElementById('light-theme-icon');
        if (newSunIcon) {
            if (!newSunIcon.dataset.rotationSetup) {
                newSunIcon.dataset.rotationSetup = 'true';
                console.log('Sun rotation setup complete - icon found');
            }
        } else {
            console.log('Sun icon not found during setup');
        }
    }

    // Initial setup
    setupSunRotation();

    // Delayed setup for Dash-rendered content
    setTimeout(setupSunRotation, 500);
    setTimeout(setupSunRotation, 1000);

    // Re-run setup when Dash updates the page
    const observer = new MutationObserver(function(mutations) {
        clearTimeout(window.sunRotationTimeout);
        window.sunRotationTimeout = setTimeout(setupSunRotation, 100);
    });

    // Observe the document for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    console.log('Sun rotation observer active');
});
