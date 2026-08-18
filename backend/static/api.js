export async function fetchSnapshots(limit) {
    const response = await fetch(
        `/api/v1/snapshots?limit=${limit}`,
        {
            cache: "no-store"
        }
    );

    if (!response.ok) {
        throw new Error(
            `Błąd HTTP: ${response.status}`
        );
    }

    return await response.json();
}