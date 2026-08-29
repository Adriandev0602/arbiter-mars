"use client";

/**
 * Panel principal: recursos disponibles, banderas condicionales activas e
 * historial de transacciones. Por ahora renderiza datos de ejemplo.
 *
 * TODO: reemplazar por un fetch real a GET /api/state/{playerId} (con
 * revalidacion cuando SidebarChat reciba una jugada aprobada).
 */
export default function Dashboard({ playerId }: { playerId: string }) {
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Estado del jugador: {playerId}</h1>

      <section className="mb-6">
        <h2 className="text-lg font-medium mb-2">Recursos</h2>
        <p className="text-gray-500 text-sm">TODO: pintar recursos reales desde Supabase</p>
      </section>

      <section className="mb-6">
        <h2 className="text-lg font-medium mb-2">Banderas condicionales activas</h2>
        <p className="text-gray-500 text-sm">TODO</p>
      </section>

      <section>
        <h2 className="text-lg font-medium mb-2">Historial de transacciones</h2>
        <p className="text-gray-500 text-sm">TODO</p>
      </section>
    </div>
  );
}
