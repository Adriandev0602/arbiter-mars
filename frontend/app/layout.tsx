import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Arbitro Asistente de Reglas",
  description: "Agente de IA para validar jugadas y calcular saldos de forma determinista",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
