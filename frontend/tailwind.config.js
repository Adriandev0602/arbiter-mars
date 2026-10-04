/** @type {import('tailwindcss').Config} */
// Tokens del mundo visual (referencia elegida por el usuario: Paymark de Lovable):
// grafito calido casi negro, acento coral, Inter Tight. Los colores de recurso
// son la semantica del propio juego (M€ dorado, acero marron, titanio gris,
// plantas verde, energia violeta, calor rojo), apagados para fondo oscuro.
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ground: "#0e0c0b",
        surface: { DEFAULT: "#171513", raised: "#1f1c19", sunk: "#121010" },
        line: { DEFAULT: "rgb(255 240 225 / 0.08)", strong: "rgb(255 240 225 / 0.14)" },
        ink: { DEFAULT: "#f5efe8", muted: "#b0a69c", faint: "#8f857b" },
        coral: { DEFAULT: "#ff6b4a", bright: "#ff8467", deep: "#e2502f", ink: "#2b0b03" },
        res: {
          mc: "#f2c14e",
          steel: "#c08a57",
          titanium: "#bdb5ac",
          plants: "#7cc463",
          energy: "#b083ee",
          heat: "#f0614f",
        },
        good: "#7cc463",
        bad: "#ff7a66",
      },
      fontFamily: {
        sans: ["var(--font-inter-tight)", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      letterSpacing: { tightish: "-0.02em", display: "-0.035em" },
      boxShadow: {
        // Boton pildora de la referencia: brillo interno arriba + sombra corta + halo calido.
        pill: "inset 0 1px 0 rgb(255 255 255 / 0.35), inset 0 -1px 0 rgb(0 0 0 / 0.18), 0 1px 2px rgb(0 0 0 / 0.45), 0 10px 24px -10px rgb(255 107 74 / 0.6)",
        "pill-quiet": "inset 0 1px 0 rgb(255 255 255 / 0.07), 0 1px 2px rgb(0 0 0 / 0.5)",
        panel: "inset 0 1px 0 rgb(255 240 225 / 0.05), 0 1px 2px rgb(0 0 0 / 0.5), 0 18px 40px -24px rgb(0 0 0 / 0.8)",
      },
      keyframes: {
        "delta-in": {
          "0%": { opacity: "0", transform: "translateY(6px) scale(0.92)", filter: "blur(2px)" },
          "100%": { opacity: "1", transform: "translateY(0) scale(1)", filter: "blur(0)" },
        },
        // Arranca en coral y vuelve al color propio del elemento (sin fijar uno final).
        "value-pulse": {
          "0%": { color: "#ff8467" },
        },
        // Un tile recien colocado en el mapa: cae en su hexagono con un borde coral que se apaga.
        "tile-in": {
          "0%": { opacity: "0", transform: "scale(0.55)", stroke: "#ff8467", "stroke-width": "4" },
          "35%": { opacity: "1", transform: "scale(1.06)" },
          "100%": { transform: "scale(1)" },
        },
      },
      animation: {
        "delta-in": "delta-in 220ms cubic-bezier(0.16, 1, 0.3, 1) both",
        "value-pulse": "value-pulse 1600ms cubic-bezier(0.16, 1, 0.3, 1) backwards",
        "tile-in": "tile-in 700ms cubic-bezier(0.16, 1, 0.3, 1) both",
      },
    },
  },
  plugins: [],
};
