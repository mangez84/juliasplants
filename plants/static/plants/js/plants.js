$("#sort-selector").change(function () {
    let currentURL = new URL(window.location);
    let selectedVal = $(this).val();

    if (selectedVal != "default") {
        let sortKey = selectedVal.split("_")[0]
        let sortDirection = selectedVal.split("_")[1]
        currentURL.searchParams.set("sort", sortKey);
        currentURL.searchParams.set("direction", sortDirection);
        window.location.replace(currentURL);
    } else {
        currentURL.searchParams.delete("sort");
        currentURL.searchParams.delete("direction");
        window.location.replace(currentURL);
    }
});