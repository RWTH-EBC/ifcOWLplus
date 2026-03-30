# IFC Plus Ontology Documentation

## Overview

The IFC Plus ontology (`ifcPlus`) extends the standard IFC4x3 ontology (`ifc`) with additional classes and properties designed to simplify queries related to building distribution systems. This extension provides direct relationships between elements that would otherwise require complex path traversals through intermediate entities in the base IFC schema.

**Namespaces:**
- `ifc:` — `http://ifcowl.openbimstandards.org/IFC4x3#`
- `ifcPlus:` — `http://ifcowl.openbimstandards.org/IFC4x3plus#`

---

## Core Classes

### ifcPlus:Device

A **Device** is an operationally relevant distribution element (e.g., pumps, valves, coils, terminals, sensors/controllers). In ifcPlus, this class is used to express **device-level functional connectivity** while abstracting away intermediate carriers.

The following IFC classes are defined as subclasses of `ifcPlus:Device`:

- `ifc:IfcFlowController` — valves, dampers, switches
- `ifc:IfcFlowTreatmentDevice` — filters, interceptors
- `ifc:IfcEnergyConversionDevice` — boilers, chillers, heat exchangers
- `ifc:IfcFlowTerminal` — outlets, fixtures, air terminals
- `ifc:IfcFlowMovingDevice` — pumps, fans, compressors
- `ifc:IfcFlowStorageDevice` — tanks, vessels
- `ifc:IfcDistributionControlElement` — sensors, controllers, actuators

### ifcPlus:FlowCarrier

A **Flow Carrier** represents passive network elements whose primary purpose is to route a medium. This includes segments and fittings (e.g., pipes/ducts and their elbows, tees, junctions).

The following IFC classes are defined as subclasses of `ifcPlus:FlowCarrier`:

- `ifc:IfcFlowSegment` — pipes, ducts, cables
- `ifc:IfcFlowFitting` — elbows, tees, junctions

Specializations:
- `ifcPlus:Pipe` — pipe segments and fittings
- `ifcPlus:Duct` — duct segments and fittings

---

## Object Properties (Shortcut Relations)

### Spatial Relationships

#### ifcPlus:HasLocation / ifcPlus:IsLocatedIn

These properties directly link distribution elements to their containing spatial structure elements (buildings, storeys, spaces) without requiring traversal through `ifc:IfcRelContainedInSpatialStructure`.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:HasLocation` | `ifc:IfcDistributionElement` | `ifc:IfcSpatialStructureElement` |
| `ifcPlus:IsLocatedIn` | `ifc:IfcSpatialStructureElement` | `ifc:IfcDistributionElement` |

These properties are inverses of each other.

### Property Set Relationships

<img src="doc/HasPropertySet.svg" width="1200">

#### ifcPlus:HasPropertySet / ifcPlus:IsPropertySetOf

In the base IFC schema, property sets are linked to objects through `ifc:IfcRelDefinesByProperties`, requiring traversal through `ifc:IsDefinedBy`, `ifc:RelatedObjects`, and `ifc:RelatingPropertyDefinition`. The `ifcPlus:HasPropertySet` property provides a direct shortcut.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:HasPropertySet` | `ifc:IfcObject` | `ifc:IfcPropertySet` |
| `ifcPlus:IsPropertySetOf` | `ifc:IfcPropertySet` | `ifc:IfcObject` |

These properties are inverses of each other.

### Port Relationships

Ports are connection points on distribution elements. IFC Plus introduces shortcut properties that directly link elements to their ports and expose **directed** port-to-port connectivity.

<img src="doc/Feeds.svg" width="1200">

#### ifcPlus:HasPort / ifcPlus:IsPortOf

The `ifcPlus:HasPort` property directly connects an `ifc:IfcDistributionElement` to its `ifc:IfcDistributionPort` instances. In the base IFC schema, this relationship requires navigating through an `ifc:IfcRelNests` entity using `ifc:IsNestedBy`, `ifc:RelatingObject`, and `ifc:RelatedObjects`.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:HasPort` | `ifc:IfcDistributionElement` | `ifc:IfcDistributionPort` |
| `ifcPlus:IsPortOf` | `ifc:IfcDistributionPort` | `ifc:IfcDistributionElement` |

These properties are inverses of each other.

#### ifcPlus:FeedsPort / ifcPlus:IsFedByPort

The `ifcPlus:FeedsPort` and `ifcPlus:IsFedByPort` properties establish directional relationships between ports based on `FlowDirection`. A port with `FlowDirection = SOURCE` is connected to a `FlowDirection = SINK` port. This shortcuts the path through `ifc:IfcRelConnectsPorts`.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:FeedsPort` | `ifc:IfcDistributionPort` | `ifc:IfcDistributionPort` |
| `ifcPlus:IsFedByPort` | `ifc:IfcDistributionPort` | `ifc:IfcDistributionPort` |

These properties are inverses of each other.

> Note: Some internal rules may additionally use port connectivity to infer element-level relations.

### Flow and Connectivity Relationships

#### ifcPlus:connectedTo / ifcPlus:isConnectedFrom (renamed from Feeds/IsFedBy)

`ifcPlus:connectedTo` provides a **directed adjacency** between two `ifc:IfcDistributionFlowElement` instances derived from port connectivity and flow direction. It abstracts away explicit traversal through `ifc:IfcRelConnectsPorts`.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:connectedTo` | `ifc:IfcDistributionFlowElement` | `ifc:IfcDistributionFlowElement` |
| `ifcPlus:isConnectedFrom` | `ifc:IfcDistributionFlowElement` | `ifc:IfcDistributionFlowElement` |

These properties are inverses of each other.

> Legacy naming: earlier versions used `ifcPlus:Feeds` / `ifcPlus:IsFedBy`. The documentation now uses `connectedTo` terminology.

#### ifcPlus:FeedsIndirectly / ifcPlus:IsFedByIndirectly

<img src="doc/ConnectsTo.svg" width="1200">

The `ifcPlus:FeedsIndirectly` property is a **transitive property** over flow carriers that expresses reachability along the carrier network.

| Property | Domain | Range | Type |
|----------|--------|-------|------|
| `ifcPlus:FeedsIndirectly` | `ifcPlus:FlowCarrier` | `ifcPlus:FlowCarrier` | `owl:TransitiveProperty` |
| `ifcPlus:IsFedByIndirectly` | `ifcPlus:FlowCarrier` | `ifcPlus:FlowCarrier` | `owl:TransitiveProperty` |

These properties are inverses of each other.

#### ifcPlus:IsConnectedTo / ifcPlus:IsConnectedFrom

These properties establish that two **devices** are functionally connected through some path of flow carriers. This collapses intermediate pipes/ducts/fittings to expose device-level dependencies.

| Property | Domain | Range |
|----------|--------|-------|
| `ifcPlus:IsConnectedTo` | `ifcPlus:Device` | `ifcPlus:Device` |
| `ifcPlus:IsConnectedFrom` | `ifcPlus:Device` | `ifcPlus:Device` |

These properties are inverses of each other.

Medium-specific subproperties:
- `ifcPlus:IsConnectedToByPipe` / `ifcPlus:IsConnectedFromByPipe`
- `ifcPlus:IsConnectedToByDuct` / `ifcPlus:IsConnectedFromByDuct`

---

## Reasoning

IFC Plus relations are derived from underlying IFC/ifcOWL patterns. In practice, inference is performed via SHACL-SPARQL rules (and OWL entailments for subclassing/transitivity). The rules materialize shortcut relations so SPARQL queries do not need to traverse verbose IFC relationship structures.

| Rule | Description |
|------|-------------|
| `ifcHasPropertySet` | Derives `ifcPlus:HasPropertySet` by traversing `ifc:IsDefinedBy` → `ifc:IfcRelDefinesByProperties` → `ifc:RelatingPropertyDefinition`. |
| `ifcHasLocation` | Derives `ifcPlus:HasLocation` by traversing `ifc:ContainsElements` → `ifc:IfcRelContainedInSpatialStructure` → `ifc:RelatedElements`. |
| `ifcHasPort` | Derives `ifcPlus:HasPort` by traversing `ifc:IsNestedBy` → `ifc:IfcRelNests` → `ifc:RelatedObjects`. |
| `ifcFeedsPortA/B` | Derives directed `ifcPlus:FeedsPort` between ports connected via `ifc:IfcRelConnectsPorts`, respecting `FlowDirection` (SOURCE → SINK). |
| `ifcConnectedTo` | Derives `ifcPlus:connectedTo` (formerly `ifcPlus:Feeds`) between distribution flow elements based on `ifcPlus:HasPort` + `ifcPlus:FeedsPort`. |
| `ifcFeedsIndirectly` | Derives `ifcPlus:FeedsIndirectly` between flow carriers. OWL transitivity then propagates reachability along carrier chains. |
| `ifcIsConnectedToDirect` | Derives `ifcPlus:IsConnectedTo` when two devices are separated by a single carrier. |
| `ifcIsConnectedToIndirect` | Derives `ifcPlus:IsConnectedTo` when two devices are separated by multiple carriers linked via `ifcPlus:FeedsIndirectly`. |

---

## Summary

IFC Plus provides convenience classes and inferred shortcut properties to simplify SPARQL queries over IFC-based knowledge graphs, especially for building automation use cases where functional connectivity and spatial context matter more than detailed routing.
