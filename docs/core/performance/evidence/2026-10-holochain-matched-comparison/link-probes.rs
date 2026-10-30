/// Explicit HDK strategy experiment on an already populated disposable conductor.
/// Times only get_links, not query construction, result comparison, or the zome roundtrip.
#[hdk_extern]
pub fn smartlink_measure_get_strategy_for_test(
    input: (LocalId, integrity_core_types::RelationshipName, u32),
) -> ExternResult<(Vec<(u32, String, u64, usize)>, Vec<String>)> {
    let (source, relationship, samples) = input;
    if !(100..=1000).contains(&samples) {
        return Err(wasm_error!(WasmErrorInner::Guest("Use 100..1000 samples".into())));
    }
    let prefix = core_types::smartlink_relationship_prefix(&relationship)
        .map_err(|error| wasm_error!(WasmErrorInner::Guest(error.to_string())))?;
    let query = LinkQuery::try_new(
        try_action_hash_from_local_id(&source).map_err(to_wasm)?,
        LinkTypes::SmartLink,
    )?
    .tag_prefix(LinkTag(prefix));
    let mut rows = Vec::new();
    let mut expected = None;
    for sample in 0..=samples {
        for position in 0..2 {
            let local = (sample + position) % 2 == 1;
            let strategy = if local { GetStrategy::Local } else { GetStrategy::default() };
            let prepared = query.clone();
            let started = sys_time()?;
            let links = get_links(prepared, strategy)?;
            let elapsed = sys_time()?.as_micros().saturating_sub(started.as_micros()) as u64;
            let mut canonical: Vec<_> = links.iter().map(|link| format!("{link:?}")).collect();
            canonical.sort();
            if let Some(expected) = &expected {
                if *expected != canonical {
                    return Err(wasm_error!(WasmErrorInner::Guest(
                        "Strategy results differ".into()
                    )));
                }
            } else {
                expected = Some(canonical);
            }
            rows.push((
                sample,
                if local { "local" } else { "default" }.into(),
                elapsed,
                links.len(),
            ));
        }
    }
    for sample in 1..=samples {
        let prepared = query.clone();
        let started = sys_time()?;
        let links = get_links(prepared, GetStrategy::Local)?;
        let elapsed = sys_time()?.as_micros().saturating_sub(started.as_micros()) as u64;
        let mut canonical: Vec<_> = links.iter().map(|link| format!("{link:?}")).collect();
        canonical.sort();
        if expected.as_ref() != Some(&canonical) {
            return Err(wasm_error!(WasmErrorInner::Guest("Repeated Local results differ".into())));
        }
        rows.push((sample, "local_repeated".into(), elapsed, links.len()));
    }
    Ok((rows, expected.unwrap_or_default()))
}

/// Rotates an empty link query and trivial host calls within one guest invocation.
#[hdk_extern]
pub fn smartlink_measure_host_baseline_for_test(
    input: (LocalId, integrity_core_types::RelationshipName, u32),
) -> ExternResult<Vec<(u32, String, u64)>> {
    let (source, relationship, samples) = input;
    if !(100..=1000).contains(&samples) {
        return Err(wasm_error!(WasmErrorInner::Guest("Use 100..1000 samples".into())));
    }
    let prefix = core_types::smartlink_relationship_prefix(&relationship)
        .map_err(|error| wasm_error!(WasmErrorInner::Guest(error.to_string())))?;
    let query = LinkQuery::try_new(
        try_action_hash_from_local_id(&source).map_err(to_wasm)?,
        LinkTypes::SmartLink,
    )?
    .tag_prefix(LinkTag(prefix));
    let operations = ["clock_pair", "sys_time", "zome_info", "empty_get_links_local"];
    let mut rows = Vec::new();
    for sample in 0..=samples {
        for offset in 0..4 {
            let operation = operations[((sample + offset) % 4) as usize];
            let prepared = query.clone();
            let started = sys_time()?;
            match operation {
                "sys_time" => {
                    let _ = sys_time()?;
                }
                "zome_info" => {
                    let _ = zome_info()?;
                }
                "empty_get_links_local" => {
                    let links = get_links(prepared, GetStrategy::Local)?;
                    if !links.is_empty() {
                        return Err(wasm_error!(WasmErrorInner::Guest(
                            "Expected an empty link bucket".into()
                        )));
                    }
                }
                _ => {}
            }
            let elapsed = sys_time()?.as_micros().saturating_sub(started.as_micros()) as u64;
            rows.push((sample, operation.into(), elapsed));
        }
    }
    Ok(rows)
}
