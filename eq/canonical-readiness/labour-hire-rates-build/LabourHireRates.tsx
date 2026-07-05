// LabourHireRates.tsx — staged reference for eq-shell src/modules/ops/
// Drop into eq-shell and confirm the import paths against the repo (createTenantDataClient
// location + Gate/HubLayout paths mirror src/pages/AdminUserList.tsx). Grounded in the
// verified eq-ui API (Table v1.4) + eq-design-tokens. No editing in v1 — read only.
//
// Two flat tables (the eq-ui Table has no nested/expandable rows):
//   1. Agencies — who we use + how to reach them
//   2. Rates    — role x rate_type x cost, per agency
//
// Reads app_data via createTenantDataClient() (tenant-scoped, RLS SELECT). cost_rate is
// sensitive — the page is gated on ops.view_rates.

import { useEffect, useState } from 'react'
import { Table, type TableColumn } from '@eq-solutions/ui'
import { Gate } from '../../permissions/Gate'
import { HubLayout } from '../../components/HubLayout'
import { createTenantDataClient } from '../../lib/tenantDataClient'

interface AgencyRow {
  company_id: string
  name: string
  primary_contact: string | null
  contact_phone: string | null
  contact_email: string | null
  payment_terms: string | null
  active: boolean
}

interface RateRow {
  rate_id: string
  company_name: string
  role: string
  rate_type: 'normal' | 'time_and_half' | 'double' | 'allowance'
  rate_label: string | null
  cost_rate: number
  unit: string
  source_doc_type: 'rate_card' | 'invoice' | 'manual'
  effective_from: string
  effective_to: string | null
  is_current: boolean
}

const RATE_TYPE_LABEL: Record<RateRow['rate_type'], string> = {
  normal: 'Normal',
  time_and_half: 'Time ½',
  double: 'Double',
  allowance: 'Allowance',
}

const SOURCE_LABEL: Record<RateRow['source_doc_type'], string> = {
  rate_card: 'Rate card',
  invoice: 'Invoice',
  manual: 'Manual',
}

function money(n: number): string {
  return `$${n.toFixed(2)}`
}

function LabourHireRatesInner() {
  const [agencies, setAgencies] = useState<AgencyRow[] | null>(null)
  const [rates, setRates] = useState<RateRow[] | null>(null)
  const [err, setErr] = useState<string | null>(null)

  const load = async () => {
    setErr(null)
    try {
      const sb = await createTenantDataClient()
      const [{ data: a, error: ae }, { data: r, error: re }] = await Promise.all([
        sb
          .from('labour_hire_companies')
          .select('company_id, name, primary_contact, contact_email, contact_phone, payment_terms, active')
          .eq('active', true)
          .order('name'),
        sb.from('labour_hire_rates_view').select('*').order('company_name'),
      ])
      if (ae) { setErr(ae.message); return }
      if (re) { setErr(re.message); return }
      setAgencies((a as AgencyRow[] | null) ?? [])
      setRates((r as RateRow[] | null) ?? [])
    } catch (e) {
      setErr((e as Error).message)
    }
  }

  useEffect(() => { void load() }, [])

  const agencyColumns: TableColumn<AgencyRow>[] = [
    { key: 'name', header: 'Agency', render: (a) => <span style={{ fontWeight: 500 }}>{a.name}</span> },
    { key: 'primary_contact', header: 'Contact', render: (a) => a.primary_contact ?? '—' },
    { key: 'contact_phone', header: 'Phone', render: (a) => a.contact_phone ?? '—' },
    {
      key: 'contact_email',
      header: 'Email',
      render: (a) =>
        a.contact_email ? <a href={`mailto:${a.contact_email}`}>{a.contact_email}</a> : '—',
    },
    { key: 'payment_terms', header: 'Terms', render: (a) => a.payment_terms ?? '—' },
  ]

  const rateColumns: TableColumn<RateRow>[] = [
    { key: 'company_name', header: 'Agency', sortAccessor: (r) => r.company_name.toLowerCase() },
    {
      key: 'role',
      header: 'Role',
      render: (r) => (
        <>
          <span>{r.role}</span>
          {r.rate_label && (
            <span className="eq-table__mute" style={{ display: 'block', fontSize: 12 }}>
              {r.rate_label}
            </span>
          )}
        </>
      ),
    },
    {
      key: 'rate_type',
      header: 'Rate type',
      sortAccessor: (r) => r.rate_type,
      render: (r) => <span className="eq-pill eq-pill--info">{RATE_TYPE_LABEL[r.rate_type]}</span>,
    },
    {
      key: 'cost_rate',
      header: 'Cost (AUD)',
      align: 'right',
      sortAccessor: (r) => r.cost_rate,
      render: (r) => (
        <span style={{ fontVariantNumeric: 'tabular-nums' }}>
          {money(r.cost_rate)}
          <span className="eq-table__mute">/{r.unit}</span>
        </span>
      ),
    },
    {
      key: 'source_doc_type',
      header: 'Source',
      sortAccessor: (r) => r.source_doc_type,
      render: (r) => (
        <span className={`eq-pill ${r.source_doc_type === 'rate_card' ? 'eq-pill--ok' : 'eq-pill--mute'}`}>
          {SOURCE_LABEL[r.source_doc_type]}
        </span>
      ),
    },
    { key: 'effective_from', header: 'Effective', sortAccessor: (r) => r.effective_from },
  ]

  return (
    <HubLayout>
      <div className="eq-page__header">
        <div>
          <h1 className="eq-page__title">Labour hire rates</h1>
          <p className="eq-page__lede">Who we use, how to reach them, and what we pay. Cost only.</p>
        </div>
      </div>

      {err && <div className="eq-empty"><p className="eq-empty__title">Couldn't load rates</p><p>{err}</p></div>}

      <section style={{ marginBottom: 'var(--eq-space-6, 24px)' }}>
        <h2 className="eq-section__title">Agencies</h2>
        <Table<AgencyRow>
          columns={agencyColumns}
          rows={agencies ?? []}
          getRowId={(a) => a.company_id}
          loading={agencies === null}
          loadingRows={3}
          defaultSort={{ key: 'name', dir: 'asc' }}
          emptyMessage="No labour hire agencies yet."
          globalSearch={{ placeholder: 'Search agencies…' }}
        />
      </section>

      <section>
        <h2 className="eq-section__title">Rates</h2>
        <Table<RateRow>
          columns={rateColumns}
          rows={rates ?? []}
          getRowId={(r) => r.rate_id}
          loading={rates === null}
          loadingRows={5}
          defaultSort={{ key: 'company_name', dir: 'asc' }}
          emptyMessage="No rates loaded yet."
          globalSearch={{ placeholder: 'Search company or role…' }}
          columnToggle
          exportable={{ filename: 'labour-hire-rates.csv' }}
          rowStyle={(r) => (r.is_current ? undefined : { opacity: 0.55 })}
          slicers={[
            { key: 'current', label: 'Current', filter: (r) => r.is_current },
            { key: 'all', label: 'All' },
            { key: 'expired', label: 'Expired', filter: (r) => !r.is_current },
          ]}
        />
      </section>
    </HubLayout>
  )
}

export default function LabourHireRates() {
  return (
    <Gate
      perm="ops.view_rates"
      fallback={
        <HubLayout>
          <div className="eq-empty">
            <p className="eq-empty__title">Not allowed</p>
            <p>Labour hire rates are visible to managers and project management.</p>
          </div>
        </HubLayout>
      }
    >
      <LabourHireRatesInner />
    </Gate>
  )
}
