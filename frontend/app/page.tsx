import Dashboard from "@/components/Dashboard";
import SidebarChat from "@/components/SidebarChat";

/**
 * Layout de dos columnas descrito en el PRD:
 * - Columna principal: dashboard con estado del jugador
 * - Sidebar derecho: chat persistente para consultar jugadas
 *
 * TODO: reemplazar el player_id hardcodeado por auth/sesion real.
 */
export default function Home() {
  const playerId = "demo-player";

  return (
    <main className="flex h-screen">
      <section className="flex-1 overflow-y-auto p-6">
        <Dashboard playerId={playerId} />
      </section>
      <aside className="w-96 border-l border-gray-200 flex flex-col">
        <SidebarChat playerId={playerId} />
      </aside>
    </main>
  );
}
