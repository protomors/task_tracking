document.addEventListener("DOMContentLoaded", () => {
    const background = document.querySelector('.background');
    const starCount = 100; // Кількість зірок

    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        
        // Випадкове розташування зірок
        star.style.width = `${Math.random() * 3 + 1}px`;
        star.style.height = star.style.width;
        star.style.left = `${Math.random() * 100}vw`;
        star.style.top = `${Math.random() * 100}vh`;
        star.style.opacity = Math.random();

        // Випадкова швидкість руху зірок
        const animationDuration = Math.random() * 5 + 5;
        star.style.animation = `moveStar ${animationDuration}s linear infinite`;
        
        background.appendChild(star);
    }
});

// Анімація руху зірок
const style = document.createElement('style');
style.innerHTML = `
@keyframes moveStar {
    0% { transform: translateY(0); }
    100% { transform: translateY(100vh); }
}
`;
document.head.appendChild(style);
