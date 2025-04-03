<script>
  let filename = "";
  let files;
</script>

<div>
  <button
    onclick={async () => {
      try {
        const response = await fetch("/list-files", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const result = await response.json();
          files = result.files;
        } else {
          throw new Error("Failed to submit data");
        }
      } catch (err) {
        console.error(err);
      }
    }}>Load Files</button
  >
</div>

{#if files}
  {#each files as file}
    <div>
      {file}
      <button
        onclick={async () => {
          try {
            const response = await fetch("/getacl", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                filename: file,
              }),
            });

            if (response.ok) {
              const result = await response.json();
              console.log(result);
            } else {
              throw new Error("Failed to get ACL data");
            }
          } catch (err) {
            console.error(err);
          }
        }}>getacl</button
      >
      <button
        onclick={async () => {
          try {
            const response = await fetch("/setacl", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                filename: file,
                user: "nobody",
                permissions: "rwx",
              }),
            });

            if (response.ok) {
              const result = await response.json();
              console.log(result);
            } else {
              throw new Error("Failed Request");
            }
          } catch (err) {
            console.error(err);
          }
        }}>setfacl</button
      >
    </div>
  {/each}
{/if}
