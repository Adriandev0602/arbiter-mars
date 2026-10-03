import "./globals.css";
import type { ReactNode } from "react";
import { Inter_Tight } from "next/font/google";

const interTight = Inter_Tight({ subsets: ["latin"], variable: "--font-inter-tight", display: "swap" });

export const metadata = {
  title: "Árbitro de Terraforming Mars",
  description: "Resuelve los cálculos de tu turno con un motor de reglas determinista: el modelo interpreta, el motor calcula.",
};

// Contrato de direccion (impeccable). Va como comentario HTML en el markup emitido.
const DIRECTION_CONTRACT = `
THESIS: el tablero de cuentas de un jugador en la mesa; lo que el motor calculo se lee de un vistazo y cada cambio se ve. Rechaza el dashboard de tarjetas iguales.
OWN-WORLD: grafito calido casi negro, acento coral solo para accion y cambio, Inter Tight de tracking cerrado, pildoras con sombra en capas, colores de recurso del propio juego.
STORY: el jugador elige corporacion y mano, juega por chat, y ve en el libro de recursos exactamente que cambio el motor.
FIRST VIEWPORT: barra con jugador; arriba a la izquierda TR y M€ grandes con produccion, al lado los otros cinco recursos; debajo la partida; a la derecha el chat con la accion primaria.
SIGNATURE INTERACTION: cuando una lectura cambia un numero del motor, ese numero late en coral y muestra su valor anterior ("antes X"), que queda visible hasta el proximo cambio; la UI no resta, muestra los dos valores del motor.
FORM: referencia fijada por el usuario (Paymark de Lovable), sin tirada de direcciones; build code-led.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
`;

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es" className={interTight.variable}>
      <body>
        <div hidden dangerouslySetInnerHTML={{ __html: `<!--${DIRECTION_CONTRACT}-->` }} />
        {children}
      </body>
    </html>
  );
}
