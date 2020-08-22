const dataSrcRootTotalMins = `${window.location.origin}/tracking/api/persona_scores_total_mins`

function getWindowElements() {
    const persona_time_elements = $(".persona_time_total")

    for (let index = 0; index < persona_time_elements.length; index++) {
        const element = persona_time_elements[index];

        appendTimeData(element.dataset.user_persona_id, element.id)
    }
}

async function getPersonaData(user_persona_id) {
    const res = await axios.get(`${dataSrcRootTotalMins}`, { params: {user_persona_id} });
    return res;
}

async function appendTimeData(user_persona_id, target_div) {
    const jsonData = await getPersonaData(user_persona_id)

    if (jsonData.data.hasOwnProperty('total_mins')) {
        $('#'+target_div).append(`<h3 class="text-info font-weight-bolder">${jsonData.data.total_mins} Mins</h3>`)
    }

}

getWindowElements()
