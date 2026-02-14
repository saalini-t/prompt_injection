import React, { useState, useEffect } from 'react';
import {
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  TableToolbar,
  TableToolbarContent,
  TableToolbarSearch,
  Tag,
  Pagination
} from '@carbon/react';

const AttackLogs = ({ showTitle = true }) => {
  const [rows, setRows] = useState([]);
  const [totalItems, setTotalItems] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLogs();
    // Refresh logs every 5 seconds
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, [page, pageSize]);

  const apiBase = import.meta.env.VITE_API_BASE_URL || '';
  const buildApiUrl = (path) => (apiBase ? `${apiBase}${path}` : path);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const skip = (page - 1) * pageSize;
      const response = await fetch(buildApiUrl(`/api/v1/simulator/logs?limit=${pageSize}&skip=${skip}`));
      const data = await response.json();
      
      // Transform MongoDB data to table format
      const transformedRows = (data.logs || []).map((log, idx) => ({
        id: log._id || idx,
        timestamp: new Date(log.timestamp * 1000).toLocaleString(),
        prompt: log.text || log.prompt || 'N/A',
        decision: log.decision || 'allow',
        confidence: ((log.confidence || 0) * 100).toFixed(0) + '%',
        mlScore: ((log.ml_score || 0) * 100).toFixed(0) + '%'
      }));
      
      setRows(transformedRows);
      setTotalItems(data.total || 0);
    } catch (error) {
      console.error('Error fetching attack logs:', error);
      setRows([]);
    } finally {
      setLoading(false);
    }
  };

  const headers = [
    { key: 'timestamp', header: 'Timestamp' },
    { key: 'prompt', header: 'Prompt' },
    { key: 'decision', header: 'Decision' },
    { key: 'confidence', header: 'Confidence' },
    { key: 'mlScore', header: 'ML Score' }
  ];

  const getDecisionTag = (decision) => {
    const types = {
      block: { type: 'red', label: 'BLOCKED' },
      sanitize: { type: 'yellow', label: 'SANITIZED' },
      allow: { type: 'green', label: 'ALLOWED' }
    };
    return types[decision] || types.allow;
  };

  return (
    <div>
      {showTitle && (
        <h2 style={{ marginBottom: '2rem' }}>Attack Logs {loading ? '(Loading...)' : ''}</h2>
      )}
      <DataTable rows={rows} headers={headers}>
        {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
          <TableContainer>
            <TableToolbar>
              <TableToolbarContent>
                <TableToolbarSearch 
                  placeholder="Search logs..." 
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </TableToolbarContent>
            </TableToolbar>
            <Table {...getTableProps()}>
              <TableHead>
                <TableRow>
                  {headers.map((header) => (
                    <TableHeader {...getHeaderProps({ header })}>
                      {header.header}
                    </TableHeader>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={headers.length} style={{ textAlign: 'center', padding: '2rem' }}>
                      {loading ? 'Loading logs...' : 'No attack logs found'}
                    </TableCell>
                  </TableRow>
                ) : (
                  rows.map((row) => {
                    const tagInfo = getDecisionTag(row.cells[2].value);
                    return (
                      <TableRow {...getRowProps({ row })}>
                        {row.cells.map((cell, index) => (
                          <TableCell key={cell.id}>
                            {index === 2 ? (
                              <Tag type={tagInfo.type} size="sm">{tagInfo.label}</Tag>
                            ) : (
                              cell.value
                            )}
                          </TableCell>
                        ))}
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </DataTable>
      <Pagination
        backwardText="Previous page"
        forwardText="Next page"
        itemsPerPageText="Items per page:"
        page={page}
        pageSize={pageSize}
        pageSizes={[10, 20, 30, 40, 50]}
        totalItems={totalItems}
        onChange={({ page, pageSize }) => {
          setPage(page);
          setPageSize(pageSize);
        }}
      />
    </div>
  );
};

export default AttackLogs;
