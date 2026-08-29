"use client";

/**
 * Sub-componente de Dashboard para pintar el inventario de recursos.
 * Separado para que sea facil de testear/reusar una vez que Dashboard
 * tenga datos reales.
 *
 * TODO: recibir props tipadas con el inventario real en vez de datos mock.
 */
export default function ResourcePanel({ resources }: { resources: Record<string, number> }) {
  const entries = Object.entries(resources ?? {});

  if (entries.length === 0) {
    return <p className="text-gray-500 text-sm">Sin recursos cargados todavia</p>;
  }

  return (
    <ul className="grid grid-cols-2 gap-2">
      {entries.map(([name, qty]) => (
        <li key={name} className="border rounded px-3 py-2 text-sm flex justify-between">
          <span className="capitalize">{name}</span>
          <span className="font-medium">{qty}</span>
        </li>
      ))}
    </ul>
  );
}
