'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { UnitKerja, UserProfile, DataRecord, LogAktivitas } from '@/types';
import { INITIAL_UNIT_KERJA, INITIAL_USERS, INITIAL_DATA_RECORDS, INITIAL_LOGS } from '@/lib/mockData';
import { supabase, isSupabaseConfigured } from '@/lib/supabase/client';

interface DataContextType {
  unitKerjas: UnitKerja[];
  users: UserProfile[];
  dataRecords: DataRecord[];
  logs: LogAktivitas[];
  currentUser: UserProfile | null;
  setCurrentUser: (user: UserProfile | null) => void;
  logout: () => void;
  isAuthLoading: boolean;
  // Data Records actions
  addDataRecord: (data: Omit<DataRecord, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateDataRecord: (id: number, data: Partial<DataRecord>) => Promise<void>;
  deleteDataRecord: (id: number) => Promise<void>;
  // Unit Kerja actions
  addUnitKerja: (unit: Omit<UnitKerja, 'id'>) => Promise<void>;
  updateUnitKerja: (id: number, unit: Partial<UnitKerja>) => Promise<void>;
  deleteUnitKerja: (id: number) => Promise<void>;
  // User actions
  addUser: (user: Omit<UserProfile, 'id'> & { password?: string }) => Promise<void>;
  updateUser: (id: string | number, user: Partial<UserProfile>) => Promise<void>;
  deleteUser: (id: string | number) => Promise<void>;
  toggleUserStatus: (id: string | number) => Promise<void>;
  resetPassword: (id: string | number, newPass: string) => Promise<void>;
  // Logs
  addLog: (aktivitas: string) => void;
  clearLogs: (keepLatest5?: boolean) => void;
  restoreSQLBackup: (sqlContent: string) => Promise<{ success: boolean; message: string }>;
  refreshCloudData: () => Promise<void>;
  isCloudConnected: boolean;
  realtimeStatus: 'connected' | 'connecting' | 'disconnected';
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [unitKerjas, setUnitKerjas] = useState<UnitKerja[]>(INITIAL_UNIT_KERJA);
  const [users, setUsers] = useState<UserProfile[]>(INITIAL_USERS);
  const [dataRecords, setDataRecords] = useState<DataRecord[]>(INITIAL_DATA_RECORDS);
  const [logs, setLogs] = useState<LogAktivitas[]>(INITIAL_LOGS);
  const [currentUser, setCurrentUserState] = useState<UserProfile | null>(null);
  const [isAuthLoading, setIsAuthLoading] = useState<boolean>(true);
  const [isCloudConnected, setIsCloudConnected] = useState<boolean>(false);
  const [realtimeStatus, setRealtimeStatus] = useState<'connected' | 'connecting' | 'disconnected'>('connecting');
  const [mounted, setMounted] = useState(false);

  // Load from LocalStorage and initial Supabase sync on mount
  useEffect(() => {
    setMounted(true);

    // One-time cleanup of stale dummy cache for production readiness
    const isCleaned = localStorage.getItem('satudata_clean_reset_v2');
    if (!isCleaned) {
      localStorage.removeItem('satudata_records');
      localStorage.removeItem('satudata_logs');
      localStorage.removeItem('satudata_units');
      localStorage.removeItem('satudata_users');
      localStorage.setItem('satudata_clean_reset_v2', 'true');
    }

    const savedUnits = localStorage.getItem('satudata_units');
    const savedUsers = localStorage.getItem('satudata_users');
    const savedData = localStorage.getItem('satudata_records');
    const savedLogs = localStorage.getItem('satudata_logs');
    const savedUser = localStorage.getItem('satudata_current_user');

    if (savedUnits) setUnitKerjas(JSON.parse(savedUnits));
    if (savedUsers) {
      try {
        const parsed = JSON.parse(savedUsers);
        const withPasswords = parsed.map((u: any) => {
          if (!u.password) {
            const init = INITIAL_USERS.find((iu) => iu.username === u.username);
            return { ...u, password: init?.password || `${u.username}#2026` };
          }
          return u;
        });
        setUsers(withPasswords);
      } catch (e) {
        setUsers(INITIAL_USERS);
      }
    }
    if (savedData) setDataRecords(JSON.parse(savedData));
    if (savedLogs) setLogs(JSON.parse(savedLogs));
    if (savedUser) {
      try {
        setCurrentUserState(JSON.parse(savedUser));
      } catch (e) {
        setCurrentUserState(null);
      }
    } else {
      setCurrentUserState(null);
    }
    setIsAuthLoading(false);

    // Fetch from Supabase if configured
    if (isSupabaseConfigured) {
      fetchSupabaseData();

      // Setup Supabase Realtime channel for live synchronization
      const channel = supabase
        .channel('satudata_realtime_hub')
        // 1. Live Data Records
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: 'data_records' },
          (payload) => {
            if (payload.eventType === 'INSERT') {
              const newRec = payload.new as DataRecord;
              setDataRecords((prev) => {
                if (prev.some((r) => r.id === newRec.id)) return prev;
                const updated = [newRec, ...prev];
                if (typeof window !== 'undefined') localStorage.setItem('satudata_records', JSON.stringify(updated));
                return updated;
              });
            } else if (payload.eventType === 'UPDATE') {
              const updatedRec = payload.new as DataRecord;
              setDataRecords((prev) => {
                const updated = prev.map((r) => (r.id === updatedRec.id ? updatedRec : r));
                if (typeof window !== 'undefined') localStorage.setItem('satudata_records', JSON.stringify(updated));
                return updated;
              });
            } else if (payload.eventType === 'DELETE') {
              const deletedId = (payload.old as { id: number }).id;
              setDataRecords((prev) => {
                const updated = prev.filter((r) => r.id !== deletedId);
                if (typeof window !== 'undefined') localStorage.setItem('satudata_records', JSON.stringify(updated));
                return updated;
              });
            }
          }
        )
        // 2. Live Unit Kerja
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: 'unit_kerja' },
          (payload) => {
            if (payload.eventType === 'INSERT') {
              const newUnit = payload.new as UnitKerja;
              setUnitKerjas((prev) => {
                if (prev.some((u) => u.id === newUnit.id)) return prev;
                const updated = [...prev, newUnit];
                if (typeof window !== 'undefined') localStorage.setItem('satudata_units', JSON.stringify(updated));
                return updated;
              });
            } else if (payload.eventType === 'UPDATE') {
              const updatedUnit = payload.new as UnitKerja;
              setUnitKerjas((prev) => {
                const updated = prev.map((u) => (u.id === updatedUnit.id ? updatedUnit : u));
                if (typeof window !== 'undefined') localStorage.setItem('satudata_units', JSON.stringify(updated));
                return updated;
              });
            } else if (payload.eventType === 'DELETE') {
              const deletedId = (payload.old as { id: number }).id;
              setUnitKerjas((prev) => {
                const updated = prev.filter((u) => u.id !== deletedId);
                if (typeof window !== 'undefined') localStorage.setItem('satudata_units', JSON.stringify(updated));
                return updated;
              });
            }
          }
        )
        // 3. Live Profiles / Users
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: 'profiles' },
          (payload) => {
            if (payload.eventType === 'INSERT' || payload.eventType === 'UPDATE') {
              const p = payload.new as any;
              const formattedUser: UserProfile = {
                id: p.id,
                nama_lengkap: p.nama_lengkap,
                nama: p.nama || p.nama_lengkap,
                username: p.username,
                email: p.email,
                role: p.role,
                unit_kerja_id: p.unit_kerja_id,
                status: p.status,
                created_at: p.created_at,
                updated_at: p.updated_at,
              };
              setUsers((prev) => {
                const exists = prev.some((u) => u.id === formattedUser.id);
                const updated = exists
                  ? prev.map((u) => (u.id === formattedUser.id ? formattedUser : u))
                  : [...prev, formattedUser];
                if (typeof window !== 'undefined') localStorage.setItem('satudata_users', JSON.stringify(updated));
                return updated;
              });
            } else if (payload.eventType === 'DELETE') {
              const deletedId = (payload.old as { id: string | number }).id;
              setUsers((prev) => {
                const updated = prev.filter((u) => u.id !== deletedId);
                if (typeof window !== 'undefined') localStorage.setItem('satudata_users', JSON.stringify(updated));
                return updated;
              });
            }
          }
        )
        // 4. Live Log Aktivitas
        .on(
          'postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'log_aktivitas' },
          (payload) => {
            const l = payload.new as any;
            const newLog: LogAktivitas = {
              id: l.id,
              user: l.username || 'System',
              aktivitas: l.aktivitas,
              tanggal: l.created_at || new Date().toISOString(),
              ip_address: l.ip_address || 'Cloud',
            };
            setLogs((prev) => {
              if (prev.some((x) => x.id === newLog.id)) return prev;
              const updated = [newLog, ...prev].slice(0, 300);
              if (typeof window !== 'undefined') localStorage.setItem('satudata_logs', JSON.stringify(updated));
              return updated;
            });
          }
        )
        .subscribe((status) => {
          if (status === 'SUBSCRIBED') {
            setRealtimeStatus('connected');
          } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
            setRealtimeStatus('disconnected');
          }
        });

      return () => {
        supabase.removeChannel(channel);
      };
    } else {
      setRealtimeStatus('disconnected');
    }
  }, []);

  const fetchSupabaseData = async () => {
    if (!isSupabaseConfigured) {
      setIsCloudConnected(false);
      setRealtimeStatus('disconnected');
      return;
    }
    try {
      const [unitsRes, profilesRes, recordsRes, logsRes] = await Promise.all([
        supabase.from('unit_kerja').select('*').order('id', { ascending: true }),
        supabase.from('profiles').select('*').order('created_at', { ascending: true }),
        supabase.from('data_records').select('*').order('id', { ascending: false }),
        supabase.from('log_aktivitas').select('*').order('created_at', { ascending: false }).limit(100),
      ]);

      // Check if network failed, DNS host not found, or project is paused
      const hasNetworkError = [unitsRes.error, profilesRes.error, recordsRes.error, logsRes.error].some(
        err => err && (
          err.message?.includes('Failed to fetch') ||
          err.details?.includes('Failed to fetch') ||
          err.message?.includes('fetch failed')
        )
      );

      if (hasNetworkError) {
        // Cloud endpoint is unreachable (offline, paused project, or unresolvable DNS)
        // Gracefully fallback to LocalStorage without throwing noisy console.error
        setIsCloudConnected(false);
        setRealtimeStatus('disconnected');
        return;
      }

      let anySuccess = false;

      if (!unitsRes.error && Array.isArray(unitsRes.data) && unitsRes.data.length > 0) {
        setUnitKerjas(unitsRes.data);
        if (typeof window !== 'undefined') localStorage.setItem('satudata_units', JSON.stringify(unitsRes.data));
        anySuccess = true;
      } else if (unitsRes.error) {
        console.warn('Supabase unit_kerja notice:', unitsRes.error.message);
      }

      if (!profilesRes.error && Array.isArray(profilesRes.data) && profilesRes.data.length > 0) {
        const formattedUsers = profilesRes.data.map(p => {
          const init = INITIAL_USERS.find(iu => iu.username.toLowerCase() === p.username.toLowerCase());
          return {
            id: p.id,
            nama_lengkap: p.nama_lengkap,
            nama: p.nama || p.nama_lengkap,
            username: p.username,
            email: p.email,
            role: p.role,
            unit_kerja_id: p.unit_kerja_id,
            status: p.status,
            password: p.password || init?.password || `${p.username}#2026`,
            created_at: p.created_at,
            updated_at: p.updated_at,
          };
        });
        setUsers(formattedUsers);
        if (typeof window !== 'undefined') localStorage.setItem('satudata_users', JSON.stringify(formattedUsers));
        anySuccess = true;
      } else if (profilesRes.error) {
        console.warn('Supabase profiles notice:', profilesRes.error.message);
      }

      if (!recordsRes.error && Array.isArray(recordsRes.data)) {
        setDataRecords(recordsRes.data);
        if (typeof window !== 'undefined') localStorage.setItem('satudata_records', JSON.stringify(recordsRes.data));
        anySuccess = true;
      } else if (recordsRes.error) {
        console.warn('Supabase data_records notice:', recordsRes.error.message);
      }

      if (!logsRes.error && Array.isArray(logsRes.data)) {
        const formattedLogs = logsRes.data.map(l => ({
          id: l.id,
          user: l.username || 'System',
          aktivitas: l.aktivitas,
          tanggal: l.created_at,
          ip_address: l.ip_address || 'Cloud',
        }));
        setLogs(formattedLogs);
        if (typeof window !== 'undefined') localStorage.setItem('satudata_logs', JSON.stringify(formattedLogs));
        anySuccess = true;
      } else if (logsRes.error) {
        console.warn('Supabase log_aktivitas notice:', logsRes.error.message);
      }

      setIsCloudConnected(anySuccess);
      setRealtimeStatus(anySuccess ? 'connected' : 'disconnected');
    } catch {
      setIsCloudConnected(false);
      setRealtimeStatus('disconnected');
    }
  };

  const setCurrentUser = (user: UserProfile | null) => {
    setCurrentUserState(user);
    if (typeof window !== 'undefined') {
      if (user) {
        localStorage.setItem('satudata_current_user', JSON.stringify(user));
        addLog(`Pengguna beralih sesi login sebagai ${user.username} (${user.role})`);
      } else {
        localStorage.removeItem('satudata_current_user');
      }
    }
  };

  const logout = () => {
    if (currentUser) {
      addLog(`User ${currentUser.username} (${currentUser.role}) keluar dari sistem (logout)`);
    }
    setCurrentUserState(null);
    if (typeof window !== 'undefined') {
      localStorage.removeItem('satudata_current_user');
    }
  };

  const addLog = (aktivitas: string) => {
    const newLog: LogAktivitas = {
      id: Date.now(),
      user: currentUser ? currentUser.username : 'Guest',
      aktivitas,
      tanggal: new Date().toISOString(),
      ip_address: '127.0.0.1',
    };
    setLogs(prev => {
      const updated = [newLog, ...prev].slice(0, 300); // keep max 300
      if (typeof window !== 'undefined') {
        localStorage.setItem('satudata_logs', JSON.stringify(updated));
      }
      return updated;
    });

    if (isSupabaseConfigured) {
      supabase.from('log_aktivitas').insert({
        username: currentUser ? currentUser.username : 'Guest',
        aktivitas,
        ip_address: '127.0.0.1',
      }).then();
    }
  };

  // Data Records CRUD
  const addDataRecord = async (data: Omit<DataRecord, 'id' | 'created_at' | 'updated_at'>) => {
    const newId = Date.now();
    const newRecord: DataRecord = {
      ...data,
      id: newId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    const updated = [newRecord, ...dataRecords];
    setDataRecords(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_records', JSON.stringify(updated));
    }
    addLog(`User ${currentUser?.username || 'Admin'} menambahkan data "${data.nama_data}"`);

    if (isSupabaseConfigured) {
      try {
        const { data: inserted } = await supabase.from('data_records').insert({
          unit_kerja_id: data.unit_kerja_id,
          nama_data: data.nama_data,
          satuan: data.satuan,
          tahun_awal: data.tahun_awal,
          jumlah: data.jumlah,
          link_gdrive: data.link_gdrive,
          deskripsi: data.deskripsi,
          status: data.status,
        }).select().single();

        if (inserted) {
          setDataRecords(prev => prev.map(r => r.id === newId ? inserted : r));
          if (typeof window !== 'undefined') {
            const synced = updated.map(r => r.id === newId ? inserted : r);
            localStorage.setItem('satudata_records', JSON.stringify(synced));
          }
        }
      } catch (err) {
        console.warn('Supabase insert record notice:', err);
      }
    }
  };

  const updateDataRecord = async (id: number, data: Partial<DataRecord>) => {
    const updated = dataRecords.map(item => 
      item.id === id ? { ...item, ...data, updated_at: new Date().toISOString() } : item
    );
    setDataRecords(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_records', JSON.stringify(updated));
    }
    addLog(`User ${currentUser?.username || 'Admin'} memperbarui data ID #${id}`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('data_records').update(data).eq('id', id);
      } catch (err) {
        console.warn('Supabase update record notice:', err);
      }
    }
  };

  const deleteDataRecord = async (id: number) => {
    const target = dataRecords.find(d => d.id === id);
    const updated = dataRecords.filter(item => item.id !== id);
    setDataRecords(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_records', JSON.stringify(updated));
    }
    addLog(`User ${currentUser?.username || 'Admin'} menghapus data "${target?.nama_data || id}"`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('data_records').delete().eq('id', id);
      } catch (err) {
        console.warn('Supabase delete record notice:', err);
      }
    }
  };

  // Unit Kerja CRUD
  const addUnitKerja = async (unit: Omit<UnitKerja, 'id'>) => {
    const newUnit: UnitKerja = { ...unit, id: Date.now() };
    const updated = [...unitKerjas, newUnit];
    setUnitKerjas(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_units', JSON.stringify(updated));
    }
    addLog(`Super Admin ${currentUser?.username || 'Admin'} menambahkan Unit Kerja baru: ${unit.nama_unit}`);

    if (isSupabaseConfigured) {
      try {
        const { data: inserted } = await supabase.from('unit_kerja').insert({
          nama_unit: unit.nama_unit,
          tipe: unit.tipe,
        }).select().single();

        if (inserted) {
          setUnitKerjas(prev => prev.map(u => u.id === newUnit.id ? inserted : u));
          if (typeof window !== 'undefined') {
            const synced = updated.map(u => u.id === newUnit.id ? inserted : u);
            localStorage.setItem('satudata_units', JSON.stringify(synced));
          }
        }
      } catch (err) {
        console.warn('Supabase insert unit notice:', err);
      }
    }
  };

  const updateUnitKerja = async (id: number, unit: Partial<UnitKerja>) => {
    const updated = unitKerjas.map(u => u.id === id ? { ...u, ...unit } : u);
    setUnitKerjas(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_units', JSON.stringify(updated));
    }
    addLog(`Super Admin ${currentUser?.username || 'Admin'} memperbarui Unit Kerja ID #${id}`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('unit_kerja').update(unit).eq('id', id);
      } catch (err) {
        console.warn('Supabase update unit notice:', err);
      }
    }
  };

  const deleteUnitKerja = async (id: number) => {
    const target = unitKerjas.find(u => u.id === id);
    if (!target) return;

    // Strict Laravel rule: cannot delete if it still has data or users
    const linkedData = dataRecords.filter(d => d.unit_kerja_id === id).length;
    const linkedUsers = users.filter(u => u.unit_kerja_id === id).length;
    if (linkedData > 0 || linkedUsers > 0) {
      throw new Error(`Unit Kerja '${target.nama_unit}' tidak dapat dihapus karena masih memiliki ${linkedData} data dan ${linkedUsers} pengguna terkait.`);
    }

    const updated = unitKerjas.filter(u => u.id !== id);
    setUnitKerjas(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_units', JSON.stringify(updated));
    }
    addLog(`Super Admin ${currentUser?.username || 'Admin'} menghapus Unit Kerja: ${target?.nama_unit}`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('unit_kerja').delete().eq('id', id);
      } catch (err) {
        console.warn('Supabase delete unit notice:', err);
      }
    }
  };

  // Users CRUD
  const addUser = async (newUser: Omit<UserProfile, 'id'> & { password?: string }) => {
    // Laravel rule: role Admin Bidang, Admin Sekretariat, Admin UPTD must have unit_kerja_id
    if (['Admin Bidang', 'Admin Sekretariat', 'Admin UPTD'].includes(newUser.role) && !newUser.unit_kerja_id) {
      throw new Error(`Unit Kerja wajib dipilih untuk peran ${newUser.role}.`);
    }

    const user: UserProfile = {
      ...newUser,
      id: Date.now(),
      password: newUser.password?.trim() || 'password123',
    };
    const updated = [...users, user];
    setUsers(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_users', JSON.stringify(updated));
    }
    addLog(`Super Admin ${currentUser?.username || 'Admin'} membuat akun pengguna baru: ${user.username} (${user.role})`);

    if (isSupabaseConfigured) {
      try {
        const { data: inserted } = await supabase.from('profiles').insert({
          nama_lengkap: user.nama_lengkap,
          nama: user.nama || user.nama_lengkap,
          username: user.username,
          email: user.email,
          role: user.role,
          unit_kerja_id: user.unit_kerja_id,
          status: user.status || 'Aktif',
        }).select().single();

        if (inserted) {
          setUsers(prev => prev.map(u => u.id === user.id ? { ...u, id: inserted.id } : u));
        }
      } catch (err) {
        console.warn('Supabase insert profile notice:', err);
      }
    }
  };

  const updateUser = async (id: string | number, data: Partial<UserProfile>) => {
    if (data.role && ['Admin Bidang', 'Admin Sekretariat', 'Admin UPTD'].includes(data.role) && !data.unit_kerja_id) {
      throw new Error(`Unit Kerja wajib dipilih untuk peran ${data.role}.`);
    }

    const updated = users.map(u => u.id === id ? { ...u, ...data } : u);
    setUsers(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_users', JSON.stringify(updated));
    }

    if (currentUser && currentUser.id === id) {
      const updatedCurrent = { ...currentUser, ...data };
      setCurrentUser(updatedCurrent);
      if (typeof window !== 'undefined') {
        localStorage.setItem('satudata_current_user', JSON.stringify(updatedCurrent));
      }
    }

    addLog(`Super Admin ${currentUser?.username || 'Admin'} memperbarui profil pengguna #${id}`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('profiles').update(data).eq('id', id);
      } catch (err) {
        console.warn('Supabase update profile notice:', err);
      }
    }
  };

  const deleteUser = async (id: string | number) => {
    // Laravel rule: cannot delete own account
    if (currentUser && id === currentUser.id) {
      throw new Error('Anda tidak dapat menghapus akun Anda sendiri.');
    }

    const target = users.find(u => u.id === id);
    const updated = users.filter(u => u.id !== id);
    setUsers(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_users', JSON.stringify(updated));
    }
    addLog(`Super Admin ${currentUser?.username || 'Admin'} menghapus akun pengguna: ${target?.username}`);

    if (isSupabaseConfigured) {
      try {
        await supabase.from('profiles').delete().eq('id', id);
      } catch (err) {
        console.warn('Supabase delete profile notice:', err);
      }
    }
  };

  const toggleUserStatus = async (id: string | number) => {
    // Laravel rule: cannot toggle own account status
    if (currentUser && id === currentUser.id) {
      throw new Error('Anda tidak dapat menonaktifkan akun Anda sendiri.');
    }

    let nextStatus: 'Aktif' | 'Nonaktif' = 'Aktif';
    const updated = users.map(u => {
      if (u.id === id) {
        const newStatus = u.status === 'Aktif' ? 'Nonaktif' : 'Aktif';
        nextStatus = newStatus as 'Aktif' | 'Nonaktif';
        addLog(`Super Admin mengubah status akun ${u.username} menjadi ${newStatus}`);
        return { ...u, status: newStatus as any };
      }
      return u;
    });
    setUsers(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_users', JSON.stringify(updated));
    }

    if (isSupabaseConfigured) {
      try {
        await supabase.from('profiles').update({ status: nextStatus }).eq('id', id);
      } catch (err) {
        console.warn('Supabase toggle status notice:', err);
      }
    }
  };

  const resetPassword = async (id: string | number, newPass: string) => {
    const target = users.find(u => u.id === id);
    const updated = users.map(u => u.id === id ? { ...u, password: newPass } : u);
    setUsers(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_users', JSON.stringify(updated));
    }
    addLog(`Super Admin mereset password akun ${target?.username}`);
  };

  const clearLogs = (keepLatest5 = false) => {
    const updated = keepLatest5 ? logs.slice(0, 5) : [];
    setLogs(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('satudata_logs', JSON.stringify(updated));
    }
    addLog(`Pembersihan riwayat audit log ${keepLatest5 ? '(menyimpan 5 log terbaru)' : 'seluruhnya'}`);
  };

  // Robust SQL value parser that respects single/double quotes, escaped quotes (''), and commas inside strings
  const parseSQLValues = (valuesStr: string): string[] => {
    const values: string[] = [];
    let current = '';
    let inString = false;
    let quoteChar = '';

    for (let i = 0; i < valuesStr.length; i++) {
      const char = valuesStr[i];
      if (inString) {
        if (char === quoteChar) {
          if (valuesStr[i + 1] === quoteChar) {
            current += quoteChar;
            i++;
          } else {
            inString = false;
          }
        } else {
          current += char;
        }
      } else {
        if (char === "'" || char === '"') {
          inString = true;
          quoteChar = char;
        } else if (char === ',') {
          values.push(current.trim());
          current = '';
        } else {
          current += char;
        }
      }
    }
    values.push(current.trim());
    return values.map(v => {
      if (v.toUpperCase() === 'NULL') return '';
      return v.replace(/^['"]|['"]$/g, '');
    });
  };

  const restoreSQLBackup = async (sqlContent: string): Promise<{ success: boolean; message: string }> => {
    try {
      if (!sqlContent || typeof sqlContent !== 'string') {
        throw new Error('Berkas SQL tidak valid.');
      }

      if (!sqlContent.includes('unit_kerja') && !sqlContent.includes('data') && !sqlContent.includes('data_records')) {
        throw new Error('Berkas bukan merupakan cadangan SQL SatuNaker DINPERINNAKER yang valid.');
      }

      const lines = sqlContent.split('\n');
      const restoredUnits: UnitKerja[] = [];
      const restoredRecords: DataRecord[] = [];
      const restoredUsers: UserProfile[] = [];

      for (const rawLine of lines) {
        const line = rawLine.trim();
        if (line.toUpperCase().startsWith('INSERT INTO')) {
          if (line.includes('unit_kerja')) {
            const match = line.match(/VALUES\s*\((.*)\);?/i);
            if (match) {
              const parts = parseSQLValues(match[1]);
              if (parts.length >= 3) {
                restoredUnits.push({
                  id: Number(parts[0]) || Date.now(),
                  nama_unit: parts[1],
                  tipe: (parts[2] as any) || 'bidang',
                });
              }
            }
          } else if (line.includes('data_records') || line.includes('`data`') || line.includes(' data ')) {
            const match = line.match(/VALUES\s*\((.*)\);?/i);
            if (match) {
              const parts = parseSQLValues(match[1]);
              if (parts.length >= 6) {
                restoredRecords.push({
                  id: Number(parts[0]) || Date.now(),
                  unit_kerja_id: Number(parts[1]) || 1,
                  nama_data: parts[2],
                  satuan: parts[3],
                  tahun_awal: Number(parts[4]) || 2026,
                  jumlah: Number(parts[5]) || 0,
                  link_gdrive: parts[6] && parts[6] !== 'NULL' && parts[6] !== '' ? parts[6] : null,
                  deskripsi: parts[7] && parts[7] !== 'NULL' && parts[7] !== '' ? parts[7] : null,
                  status: (parts[8] as any) || 'Aktif',
                  created_by: currentUser?.nama_lengkap || 'Super Admin',
                  created_at: new Date().toISOString(),
                });
              }
            }
          } else if (line.includes('profiles') || line.includes('users')) {
            const match = line.match(/VALUES\s*\((.*)\);?/i);
            if (match) {
              const parts = parseSQLValues(match[1]);
              if (parts.length >= 5) {
                restoredUsers.push({
                  id: parts[0] || Date.now().toString(),
                  nama_lengkap: parts[1] || parts[2],
                  nama: parts[1] || parts[2],
                  username: parts[2] || parts[1],
                  email: parts[3],
                  role: (parts[4] as any) || 'Admin Bidang',
                  unit_kerja_id: parts[5] && parts[5] !== '' && parts[5] !== 'NULL' ? Number(parts[5]) : null,
                  status: (parts[6] as any) || 'Aktif',
                  password: `${parts[2]}#2026`,
                });
              }
            }
          }
        }
      }

      if (restoredUnits.length > 0) {
        setUnitKerjas(restoredUnits);
        localStorage.setItem('satudata_units', JSON.stringify(restoredUnits));
      }
      if (restoredRecords.length > 0) {
        setDataRecords(restoredRecords);
        localStorage.setItem('satudata_records', JSON.stringify(restoredRecords));
      }
      if (restoredUsers.length > 0) {
        setUsers(restoredUsers);
        localStorage.setItem('satudata_users', JSON.stringify(restoredUsers));
      }

      addLog(`Super Admin memulihkan (restore) database dari berkas SQL cadangan (${restoredUnits.length} unit, ${restoredRecords.length} data, ${restoredUsers.length} pengguna)`);
      return {
        success: true,
        message: `Basis data berhasil dipulihkan! (${restoredUnits.length} unit kerja, ${restoredRecords.length} data sektoral${restoredUsers.length > 0 ? `, ${restoredUsers.length} akun pengguna` : ''})`,
      };
    } catch (err: any) {
      return {
        success: false,
        message: err.message || 'Gagal memulihkan database dari file SQL.',
      };
    }
  };

  return (
    <DataContext.Provider
      value={{
        unitKerjas,
        users,
        dataRecords,
        logs,
        currentUser,
        setCurrentUser,
        logout,
        isAuthLoading,
        addDataRecord,
        updateDataRecord,
        deleteDataRecord,
        addUnitKerja,
        updateUnitKerja,
        deleteUnitKerja,
        addUser,
        updateUser,
        deleteUser,
        toggleUserStatus,
        resetPassword,
        addLog,
        clearLogs,
        restoreSQLBackup,
        refreshCloudData: fetchSupabaseData,
        isCloudConnected,
        realtimeStatus,
      }}
    >
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
}
